from web3 import Web3
import json
import os

# Connect to local Ganache blockchain
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ganache")

# Load contract
def load_contract():
    contract_path = os.path.join(os.path.dirname(__file__), '../contracts/ToDoManager.json')  # ABI JSON file
    with open(contract_path) as f:
        contract_data = json.load(f)
    
    contract_address = contract_data['networks']['5777']['address']
    abi = contract_data['abi']
    
    contract = web3.eth.contract(address=contract_address, abi=abi)
    return contract
