from solcx import compile_standard, install_solc
from web3 import Web3
import json
import os

# 1. Install and set compiler version
install_solc("0.8.0")

# 2. Load Solidity code
with open("contracts/ToDoManager.sol", "r") as file:
    contract_source_code = file.read()

# 3. Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "ToDoManager.sol": {
            "content": contract_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.0")

# 4. Save ABI and Bytecode
abi = compiled_sol['contracts']['ToDoManager.sol']['ToDoManager']['abi']
bytecode = compiled_sol['contracts']['ToDoManager.sol']['ToDoManager']['evm']['bytecode']['object']

# 5. Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    raise ConnectionError("Failed to connect to Ganache")

# 6. Get default account
web3.eth.default_account = web3.eth.accounts[0]

# 7. Deploy the contract
ToDoManager = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = ToDoManager.constructor().transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract deployed at address:", tx_receipt.contractAddress)

# 8. Save ABI and address to JSON
output = {
    "abi": abi,
    "networks": {
        "5777": {
            "address": tx_receipt.contractAddress
        }
    }
}

with open("contracts/ToDoManager.json", "w") as f:
    json.dump(output, f, indent=4)

print("ToDoManager.json generated successfully.")
