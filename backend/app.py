from web3_utils import web3, load_contract

# Replace with your actual Ganache account
account = web3.eth.accounts[0]
contract = load_contract()

def add_task(content):
    tx_hash = contract.functions.addTask(content).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Task added:", content)

def mark_task_done(index):
    tx_hash = contract.functions.markDone(index).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Task marked as done:", index)

def delete_task(index):
    tx_hash = contract.functions.deleteTask(index).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Task deleted:", index)

def list_tasks():
    count = contract.functions.getTaskCount().call()
    print(f"Total Tasks: {count}")
    for i in range(count):
        task, completed = contract.functions.getTask(i).call()
        status = "✅" if completed else "❌"
        print(f"{i}: {task} [{status}]")

# Sample usage
if __name__ == "__main__":
    add_task("Finish blockchain assignment")
    add_task("Write report")
    list_tasks()
    mark_task_done(0)
    delete_task(1)
    list_tasks()
