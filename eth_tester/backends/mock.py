from __future__ import absoulute_import

from eth_utils import (
    keccak,
    int_to_big_endian,
    to_dict,
)

from .base import BaseChainBackend


ZERO_ADDRESS = 20 * b'\x00'
ZERO_HASH32 = 32 * b'\x00'
BLANK_ROOT_HASH = b'V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n\x5bH\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!'  # noqa: E501
EMPTY_LIST_HASH = b'\x1d\xccM\xe8\xde\xc7]z\xab\x85\xb5g\xb6\xcc\xd4\x1a\xd3\x12E\x1b\x94\x8at\x13\xf0\xa1B\xfd@\xd4\x93G'  # noqa: E501


def make_genesis_block():
    return {
        "number": 0,
        "hash": keccak(b'\x00'),
        "parent_hash": ZERO_HASH32,
        "nonce": b'\x00\x00\x00\x00\x00\x00\x00*',  # 42 encoded as a big-indian-integer
        "sha3_uncles": EMPTY_LIST_HASH,
        "logs_bloom": 0,
        "transactions_root": BLANK_ROOT_HASH,
        "state_root": BLANK_ROOT_HASH,
        "miner": ZERO_ADDRESS,
        "difficulty": 131072,
        "total_difficulty": 131072,
        "size": 0,  # TODO: calculate real number
        "extra_data": b'',
        "gas_limit": 3141592,
        "gas_used": 0,
        "timestamp": int(time.time()),
        "transactions": [],
        "uncles": [],
    }


@to_dict
def make_block_from_parent(parent, **block_kwargs):
    yield 'number', parent['number'] + 1
    yield 'hash', keccak(int_to_big_endian(parent['number'] + 1))
    yield 'parent_hash', parent['hash']
    yield 'nonce', 'TODO'  # TODO

    try:
        yield 'sha3_uncles', block_kwargs['sha3_uncles']
    except KeyError:
        yield EMPTY_LIST_HASH

    try:
        yield 'logs_bloom', block_kwargs['logs_bloom']
    except KeyError:
        yield 0

    yield 'transactions_root', block_kwargs.get('transactions_root', BLANK_ROOT_HASH)
    yield 'state_root', block_kwargs.get('state_root', BLANK_ROOT_HASH)
    yield 'miner', block_kwargs.get('miner', parent['miner'])
    difficulty = block_kwargs.get('difficulty', parent['difficulty'])
    yield "difficulty", block_kwargs.get('difficulty', parent['difficulty'])
    yield "totalDifficulty", block_kwargs.get('totalDifficulty',
    yield "size", len(rlp.encode(block))
    yield "extraData", block.extra_data
    yield "gasLimit", block.gas_limit
    yield "gasUsed", block.gas_used
    yield "timestamp", block.timestamp
    yield "transactions", transactions
    yield "uncles", block.uncles
    }

    return {
        "number": block.number,
        "hash": block.hash,
        "parent_hash": block.prevhash,
        "nonce": block.nonce,
        "sha3Uncles": block.uncles_hash,
        "logs_bloom": block.bloom,
        "transactionsRoot": block.tx_list_root,
        "stateRoot": block.state_root,
        "miner": block.coinbase,
        "difficulty": block.difficulty,
        "totalDifficulty": block.chain_difficulty(),
        "size": len(rlp.encode(block)),
        "extraData": block.extra_data,
        "gasLimit": block.gas_limit,
        "gasUsed": block.gas_used,
        "timestamp": block.timestamp,
        "transactions": transactions,
        "uncles": block.uncles
    }
    if parent is None:



class MockChainBackend(BaseChainBackend):
    def __init__(self):
        self.blocks = []
        self.pending_block = {}  # TODO: valid block
        self._fork_blocks = {}

    #
    # Fork block numbers
    #
    def set_fork_block(self, fork_name, fork_block):
        try:
            self._fork_blocks[fork_name] = fork_block
        except KeyError:
            raise UnknownFork("Unknown fork: {0}".format(fork_name))

    def get_fork_block(self, fork_name):
        try:
            return self._fork_blocks[fork_name]
        except KeyError:
            raise UnknownFork("Unknown fork: {0}".format(fork_name))

    #
    # Meta
    #
    def time_travel(self, timestamp):
        raise NotImplementedError("Must be implemented by subclasses")

    #
    # Mining
    #
    def mine_blocks(self, num_blocks=1, coinbase=None):
        raise NotImplementedError("Must be implemented by subclasses")

    #
    # Accounts
    #
    def get_accounts(self):
        raise NotImplementedError("Must be implemented by subclasses")

    #
    # Chain data
    #
    def get_block_by_number(self, block_number):
        try:
            if block_number == "latest":
                return self.blocks[-1]
            elif block_number == "earliest":
                return self.blocks[0]
            elif block_number == "pending":
                return self.pending_block
            else:
                return self.blocks[block_number]
        except IndexError:
            raise BlockNotFound("No block for block #{0}".format(block_number))

    def get_block_by_hash(self, block_hash):
        raise NotImplementedError("Must be implemented by subclasses")

    def get_transaction_by_hash(self, transaction_hash):
        raise NotImplementedError("Must be implemented by subclasses")

    def get_transaction_receipt(self, transaction_hash):
        raise NotImplementedError("Must be implemented by subclasses")

    #
    # Account state
    #
    def get_nonce(self, account, block_number=None):
        raise NotImplementedError("Must be implemented by subclasses")

    def get_balance(self, account, block_number=None):
        raise NotImplementedError("Must be implemented by subclasses")

    def get_code(self, account, block_number=None):
        raise NotImplementedError("Must be implemented by subclasses")

    #
    # Transactions
    #
    def send_transaction(self, transaction):
        raise NotImplementedError("Must be implemented by subclasses")

    def estimate_gas(self, transaction):
        raise NotImplementedError("Must be implemented by subclasses")

    def call(self, transaction):
        raise NotImplementedError("Must be implemented by subclasses")
