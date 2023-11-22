import click
from utils import (
    basic as my_basic,
    crypto as my_crypto
)

@click.group()
def cli():
    pass


@click.command()
@click.option('--wallet', 'wallet_', type=str, default=None, required=True, prompt='location of a wallet file', help='location of a wallet file')
@click.option('--network', 'network_', type=str, default=None, required=True, prompt='url of a vechain node to send tx', help='url of a vechain node to send tx')
@click.option('--factory-file', 'factory_file_', type=str, default=None, required=True, prompt='location of a compiled factory file', help='location of a compiled factory file')
@click.option('--factory-addr', 'factory_addr_', type=str, default=None, required=True, prompt='deployed factory address on-chain', help='deployed factory address on-chain')
@click.option('--token0-addr', 'token0_addr_', type=str, default=None, required=True, prompt='deployed token0 address on-chain', help='deployed token0 address on-chain')
@click.option('--token1-addr', 'token1_addr_', type=str, default=None, required=True, prompt='deployed token1 address on-chain', help='deployed token1 address on-chain')
def create_pool(wallet_, network_, factory_file_, factory_addr_, token0_addr_, token1_addr_):
    '''Create a pool of two VIP-180 tokens on VeRocket DEX
    '''
    wallet = my_crypto.load_wallet(wallet_)
    connector = my_crypto.load_connector(network_)
    factory_contract = my_crypto.load_contract(factory_file_)

    # Check contracts existence
    my_crypto.not_smart_contract_then_raise(connector, factory_addr_)
    my_crypto.not_smart_contract_then_raise(connector, token0_addr_)
    my_crypto.not_smart_contract_then_raise(connector, token1_addr_)

    # Call "createPair" to make new pool over token0 and token1
    # Call on factory to create a pool of token 1 and token 2
    response = connector.transact(wallet, factory_contract, 'createPair', [token0_addr_, token1_addr_], factory_addr_)
    tx_id = response['id']

    # No receipt then raise
    receipt = my_crypto.wait_for_receipt_or_raise(connector, tx_id)
    # Not successful then raise
    my_crypto.if_reverted_then_raise(connector, receipt, tx_id)

    # Sucessful, output tx id and newly created pool address
    response = connector.call(wallet.getAddress(), factory_contract, 'getPair', [token0_addr_, token1_addr_], factory_addr_)
    print(f"pool address: {response['decoded']['0']}")

    l = sorted([str(token0_addr_).lower(), str(token1_addr_).lower()])
    print(f"token 0 of pool: {l[0]}")
    print(f"token 1 of pool: {l[1]}")

    print(f"tx_id: {tx_id}")


# def deposit_token_and_token():
#     '''Deposit two VIP-180 tokens into a pool on VeRocket '''
#     pass


# def deposit_vet_and_token():
#     ''' Deposit VET and a VIP-180 token into a pool on VeRocket '''
#     pass


@click.command()
@click.option('--json', 'json_', type=str, default=None, required=True, prompt="location of solidity compiled file (json)", help='location of solidity compiled file (json)')
def init_code_hash(json_):
    '''
        Calculate "init code hash" for a solidity compiled file.
        This is used when a dev tweaked the UniswapV2Pair.sol and re-compile.
        Fill this value into UniswapV2Library.sol.
    '''
    _smart_contract = my_crypto.load_contract(json_)
    init_code_hash_hex = my_crypto.calc_init_code_hash(_smart_contract.get_bytecode())
    print(f'file: {json_} \ninit code hash (for CREATE2):', init_code_hash_hex)


# @click.command()
# @click.option('--network', 'network_', type=str, default=None, required=True, prompt="VeChain thor node URL", help="VeChain thor node URL")
# @click.option('--wallet', 'wallet_', type=str, default=None, required=True, prompt='', help='')
# @click.option('--token-file', 'token_file_', type=str, default=None, required=True, prompt='location of a compiled token file', help='location of a compiled token file')
# def deploy_token(network_, wallet_, token_file_):
#     '''
#         Deploy your token onto vechain. Feed-in a solidity compiled file
#     '''
#     pass


# @click.option()
# def create_factory_router():
#     '''Deploy VeRocket factory (used to create pools) and router02 (user interaction point)
#     '''
#     pass


cli.add_command(init_code_hash)
cli.add_command(create_pool)


if __name__ == '__main__':
    cli()
