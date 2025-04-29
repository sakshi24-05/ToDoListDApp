# ToDoList DApp

A decentralized To-Do List application built using **Python (Tkinter GUI)**, **Ethereum Smart Contracts (Solidity)**, and **Web3.py**.  
This project demonstrates full-stack DApp development with blockchain integration, local UI, and version control support.

---

## 📌 Features

- 🔐 PIN-protected access (default: `1234`)
- 🗓️ Add tasks with deadline **date & time**
- 🧠 Automatic grouping into:
  - **Today**
  - **Tomorrow**
  - **Upcoming**
  - ✅ **Completed**
- 🪙 Logs every task to Ethereum via Ganache
- 🔁 Transaction hash and block confirmation shown
- 📤 Export task list to `.txt`
- 💾 Version controlled with Git

---

## 📂 Project Structure

```
ToDoListDApp/
├── backend/
│   ├── deploy_contract.py       # Deploys Solidity contract
│   ├── web3_utils.py            # Connects to blockchain
├── frontend/
│   └── main.py                  # Tkinter GUI application
├── contracts/
│   └── ToDoManager.sol          # Solidity smart contract
├── report.pdf                   # Technical report
├── requirements.txt             # Python dependencies
├── README.md                    # You are here
└── .gitignore
```

---

## 💡 Technologies Used

| Layer          | Technology               |
|----------------|---------------------------|
| Frontend       | Python Tkinter            |
| Smart Contract | Solidity                  |
| Blockchain     | Ganache (Local Ethereum)  |
| Python Web3    | web3.py                   |
| Versioning     | Git                       |

---

## 🚀 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ToDoListDApp.git
cd ToDoListDApp
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ganache & Deploy Smart Contract

```bash
python backend/deploy_contract.py
```

### 4. Run the GUI app

```bash
python frontend/main.py
```

---

## 🧪 Screenshots

📌 *Add screenshots here or paste them directly in GitHub.*

---

## 🎓 Author

**Sakshi kothmarivala**  
University of East London  
Module: CN6035 - DApp Development  
Lecturer: Dr. _____

---

## 📜 License

MIT License © 2025
