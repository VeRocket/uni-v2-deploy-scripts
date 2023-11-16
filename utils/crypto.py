# Crypto related functions
from typing import Union
from thor_devkit import cry
from thor_requests import utils
from thor_requests.wallet import Wallet
from thor_requests.connect import Connect
from thor_requests.contract import Contract
from .basic import read_json_file


WAIT_TIME_LIMIT = 60 # Wait up to 60 seconds


def calc_init_code_hash(content: bytes, output_flag_hex: bool=True) -> Union[bytes, str]:
    '''Calculate the init code hash of a given smart contract bytes.

    Args:
        content (bytes): smart contract compiled bytes.
        output_flag_hex (bool, optional): output of the function shall in hex string (True), or pure bytes (False). Defaults to True.

    Returns:
        Union[bytes, str]: bytes or hex string
    '''
    digest, _ = cry.keccak256([content])
    if output_flag_hex:
        return digest.hex()
    else:
        return digest


def load_wallet(path_like: str) -> Wallet:
    '''Load a wallet from a given path

    Args:
        path_like (str): path of the wallet

    Raises:
        Exception: If wallet is ill-formed

    Returns:
        Wallet: A usable wallet
    '''
    j = read_json_file(path_like)
    w = None
    if j.get('private_key'):
        w = Wallet.fromPrivateKey(bytes.fromhex(j['private_key']))
    elif j.get('words'):
        w = Wallet.fromMnemonic(j['words'])
    elif j.get('crypto') and j.get('id') and j.get('version'):
        w = Wallet.fromKeyStore(j)
    else:
        raise Exception("Wallet isn't one of private_key, mnemonic or keystore style.")
    return w


def load_connector(url: str) -> Connect:
    '''Load a VeChain Connector from URL

    Args:
        url (str): VeChain thor node URL

    Returns:
        Connect: A connector
    '''
    return Connect(url)


def load_contract(path_like: str) -> Contract:
    '''Load a smart contract from a file

    Args:
        path_like (str): location of a compiled smart contract file.

    Returns:
        Contract: A smart contract object
    '''
    return Contract.fromFile(path_like)


def is_smart_contract(c: Connect, address: str) -> bool:
    '''Check if the given address is a smart contract on-chain.

    Args:
        c (Connect): A connector to VeChain
        address (str): The address in question

    Returns:
        bool: True if is a smart contract, otherwise false.
    '''
    return utils.is_contract(c.get_account(address))


def not_smart_contract_then_raise(c: Connect, address: str):
    '''If not smart contract will causing an exception

    Args:
        c (Connect): a connector to VeChain
        address (str): the address in interest.
    '''
    if not is_smart_contract(c, address):
        raise Exception(f"{address} is not a smart contract")


def wait_for_receipt_or_raise(c: Connect, tx_id: str, wait_limit:int=WAIT_TIME_LIMIT) -> dict:
    # Wait for Receipt (Can be success or failure receipt)
    receipt = c.wait_for_tx_receipt(tx_id, wait_limit)
    if not receipt:
        raise Exception(f"receipt not found by tx id: {tx_id}")
    return receipt


def if_reverted_then_raise(c: Connect, receipt: dict, tx_id: str):
    if utils.is_reverted(receipt):
        # explain the reason
        print(c.replay_tx(tx_id))
        raise Exception(f"{tx_id} is reverted!")