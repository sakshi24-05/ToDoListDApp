import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, font, ttk
from threading import Thread
from time import sleep
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from web3_utils import web3, load_contract

contract = load_contract()
account = web3.eth.accounts[0]
contract_address = contract.address
network_name = "Ganache Localhost (ID 5777)"

# Local task storage
tasks = []
last_tx_hash = ""

# GUI setup
root = tk.Tk()
root.title("🪙 Blockchain To-Do List DApp (Grouped by Date)")
root.geometry("1000x700")
root.configure(bg="#fdfdfd")
font_style = font.Font(family="Segoe UI", size=10)

# PIN Login Screen
def login_screen():
    login_root = tk.Toplevel()
    login_root.title("🔐 Login - Blockchain DApp")
    login_root.geometry("300x150")
    login_root.configure(bg="#fdfdfd")

    tk.Label(login_root, text="Enter PIN to Access", font=("Segoe UI", 12), bg="#fdfdfd").pack(pady=10)
    pin_var = tk.StringVar()
    pin_entry = tk.Entry(login_root, textvariable=pin_var, show="*", font=("Segoe UI", 12))
    pin_entry.pack()

    attempts = [0]

    def check_pin():
        if pin_var.get() == "1234":
            login_root.destroy()
        else:
            attempts[0] += 1
            if attempts[0] >= 3:
                messagebox.showerror("Access Denied", "Too many wrong attempts.")
                login_root.destroy()
                root.destroy()
            else:
                messagebox.showwarning("Incorrect PIN", f"Wrong PIN! Attempts left: {3 - attempts[0]}")

    tk.Button(login_root, text="Login", font=("Segoe UI", 12), bg="#dcedc8", command=check_pin).pack(pady=10)
    login_root.transient(root)
    login_root.grab_set()
    root.wait_window(login_root)

# Helper Functions
def run_transaction(action, *args):
    global last_tx_hash
    status_label.config(text="⏳ Waiting for blockchain confirmation...", fg="blue")

    def task():
        try:
            tx_hash = action(*args)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            last_tx_hash = tx_hash.hex()

            # Format blockchain message
            message = (
                "✅ Sent to Blockchain:\n"
                f"• TX Hash: {last_tx_hash}\n"
                f"• Block #: {receipt.blockNumber}"
            )

            # GUI updates (on main thread)
            root.after(0, update_tx_hash)
            root.after(0, refresh_tasks)
            root.after(0, lambda: messagebox.showinfo("Blockchain Save Successful!", message))
            root.after(0, lambda: status_label.config(text="✅ Operation successful", fg="green"))

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Blockchain Error", str(e)))
            root.after(0, lambda: status_label.config(text="❌ Operation failed", fg="red"))

        sleep(1.5)
        root.after(0, lambda: status_label.config(text=""))

    Thread(target=task).start()



def update_tx_hash():
    tx_label.config(text=f"Last Transaction Hash: {last_tx_hash}")

def refresh_tasks():
    today_list.delete(0, tk.END)
    tomorrow_list.delete(0, tk.END)
    upcoming_list.delete(0, tk.END)
    completed_list.delete(0, tk.END)

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    after = today + timedelta(days=3)

    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d %H:%M'))
    for idx, t in enumerate(sorted_tasks):
        try:
            due = datetime.strptime(t['deadline'], '%Y-%m-%d %H:%M')
        except ValueError:
            continue
        line = f"{idx}: {t['task']} [{t['priority']}] - Due: {t['deadline']}"
        if t['completed']:
            completed_list.insert(tk.END, line)
        elif due.date() == today:
            today_list.insert(tk.END, line)
        elif due.date() == tomorrow:
            tomorrow_list.insert(tk.END, line)
        elif today < due.date() <= after:
            upcoming_list.insert(tk.END, line)

def add_task_blockchain(content):
    tx_hash = contract.functions.addTask(content).transact({'from': account})
    return tx_hash

def mark_done_blockchain(index):
    tx_hash = contract.functions.markDone(index).transact({'from': account})
    return tx_hash

def delete_task_blockchain(index):
    tx_hash = contract.functions.deleteTask(index).transact({'from': account})
    return tx_hash

# GUI Functions
def add_task():
    task_name = task_entry.get()
    deadline = deadline_entry.get()
    priority = priority_var.get()

    if not task_name or not deadline or not priority:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        datetime.strptime(deadline, '%Y-%m-%d %H:%M')
    except ValueError:
        messagebox.showwarning("Date Error", "Use format: YYYY-MM-DD HH:MM")
        return

    new_task = {"task": task_name, "deadline": deadline, "priority": priority, "completed": False}
    tasks.append(new_task)
    run_transaction(add_task_blockchain, task_name)
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)

def mark_done():
    for listbox in [today_list, tomorrow_list, upcoming_list]:
        selected = listbox.curselection()
        if selected:
            idx = int(listbox.get(selected[0]).split(":")[0])
            tasks[idx]['completed'] = True
            run_transaction(mark_done_blockchain, idx)
            return

def delete_task():
    for listbox in [today_list, tomorrow_list, upcoming_list, completed_list]:
        selected = listbox.curselection()
        if selected:
            idx = int(listbox.get(selected[0]).split(":")[0])
            tasks.pop(idx)
            run_transaction(delete_task_blockchain, idx)
            return

# Start Login Check
login_screen()

# GUI Build
info_frame = tk.Frame(root, bg="#fdfdfd")
info_frame.pack(pady=(10, 5))

for text in [f"Connected Account: {account}", f"Smart Contract Address: {contract_address}", f"Network: {network_name}"]:
    tk.Label(info_frame, text=text, font=font_style, bg="#fdfdfd", fg="gray").pack()

# Input Area
top_frame = tk.Frame(root, bg="#fdfdfd")
top_frame.pack(padx=10, pady=10)

middle_frame = tk.Frame(root, bg="#fdfdfd")
middle_frame.pack(padx=10, pady=5)

bottom_frame = tk.Frame(root, bg="#fdfdfd")
bottom_frame.pack(padx=10, pady=10)

task_entry = tk.Entry(top_frame, font=font_style, width=30)
task_entry.grid(row=0, column=0, padx=5)

deadline_entry = tk.Entry(top_frame, font=font_style, width=20)
deadline_entry.grid(row=0, column=1, padx=5)
deadline_entry.insert(0, "YYYY-MM-DD HH:MM")

priority_var = tk.StringVar()
priority_dropdown = ttk.Combobox(top_frame, textvariable=priority_var, values=["High", "Medium", "Low"], font=font_style, width=10)
priority_dropdown.grid(row=0, column=2, padx=5)

add_button = tk.Button(top_frame, text="➕ Add Task", font=font_style, command=add_task, bg="#e0f7fa")
add_button.grid(row=0, column=3, padx=5)

# Section Headers
headers = ["Today", "Tomorrow", "Upcoming", "Completed"]
listboxes = []
for i, label in enumerate(headers):
    tk.Label(middle_frame, text=label, font=font_style, bg="#fdfdfd").grid(row=0, column=i)
    lb = tk.Listbox(middle_frame, font=font_style, width=25, height=15)
    lb.grid(row=1, column=i, padx=5)
    listboxes.append(lb)

today_list, tomorrow_list, upcoming_list, completed_list = listboxes

# Bottom Buttons
mark_done_button = tk.Button(bottom_frame, text="✅ Mark Done", font=font_style, command=mark_done, bg="#dcedc8")
mark_done_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(bottom_frame, text="❌ Delete Task", font=font_style, command=delete_task, bg="#ffcdd2")
delete_button.grid(row=0, column=1, padx=5)

status_label = tk.Label(root, text="", font=font_style, fg="blue", bg="#fdfdfd")
status_label.pack(pady=(0, 5))

badge = tk.Label(root, text="🛡️ Secured by Ethereum Smart Contract", font=("Arial", 10), fg="black")
badge.pack(side="bottom", pady=5)

refresh_tasks()
root.mainloop()