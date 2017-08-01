from __future__ import unicode_literals

from cytoolz import (
    partial,
)

from eth_utils import (
    is_boolean,
    is_integer,
    is_string,
    is_hex,
    is_text,
    remove_0x_prefix,
    is_hex_address,
    is_checksum_formatted_address,
    is_checksum_address,
    is_list_like,
)

from eth_tester.constants import (
    BLOCK_NUMBER_META_VALUES,
)
from eth_tester.exceptions import (
    ValidationError,
)

from .base import BaseValidationBackend


def validate_positive_integer(value, name):
    error_message = "{0} values must be positive integers.  Got: {1}".format(
        name,
        value,
    )
    if not is_integer(value) or is_boolean(value):
        raise ValidationError(error_message)
    elif value < 0:
        raise ValidationError(error_message)


def validate_32_byte_hex_value(value, name):
    error_message = (
        "{0} must be a hexidecimal encoded 32 byte string.  Got: "
        "{1}".format(name, value)
    )
    if not is_text(value):
        raise ValidationError(error_message)
    elif not is_hex(value):
        raise ValidationError(error_message)
    elif len(remove_0x_prefix(value)) != 64:
        raise ValidationError(error_message)


MAX_TIMESTAMP = 33040162800  # January 1st 3017 is appropriately far in the future.


def validate_timestamp(value):
    validate_positive_integer(value, name="Timestamp")

    if value >= MAX_TIMESTAMP:
        raise ValidationError(
            "Timestamp values must be less than {0}.  Got {1}".format(
                MAX_TIMESTAMP,
                value,
            )
        )


def validate_block_number(value):
    error_message = (
        "Block number must be a positive integer or one of the strings "
        "'latest', 'earliest', or 'pending'.  Got: {0}".format(value)
    )
    if is_string(value):
        if value not in BLOCK_NUMBER_META_VALUES:
            raise ValidationError(error_message)
    elif not is_integer(value) or is_boolean(value):
        raise ValidationError(error_message)
    elif value < 0:
        raise ValidationError(error_message)


validate_block_hash = partial(validate_32_byte_hex_value, name="Block hash")
validate_transaction_hash = partial(validate_32_byte_hex_value, name="Transaction hash")
validate_filter_id = partial(validate_positive_integer, name="Filter ID")


def validate_address(value):
    if not is_text(value):
        raise ValidationError("Address must be 20 bytes encoded as hexidecimal")
    elif not is_hex_address(value):
        raise ValidationError("Address must be 20 bytes encoded as hexidecimal")
    elif is_checksum_formatted_address(value) and not is_checksum_address(value):
        raise ValidationError("Address does not validate EIP55 checksum")


def validate_filter_params(from_block, to_block, address, topics):
    if from_block is not None:
        validate_block_number(from_block)
    if to_block is not None:
        validate_block_number(to_block)

    if is_list_like(address):
        if not address:
            raise ValidationError(
                "Address must be either a single hexidecimal encoded address or "
                "a non-empty list of hexidecimal encoded addresses"
            )
        for sub_address in address:
            validate_address(sub_address)
    elif not is_hex_address(address):
        validate_address(address)

    assert False, "TODO: topic array"



class StrictValidationBackend(BaseValidationBackend):
    validate_timestamp = staticmethod(validate_timestamp)
    validate_block_number = staticmethod(validate_block_number)
    validate_block_hash = staticmethod(validate_block_hash)
    validate_transaction_hash = staticmethod(validate_transaction_hash)
    validate_filter_id = staticmethod(validate_filter_id)
