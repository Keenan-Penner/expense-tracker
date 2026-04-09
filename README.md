# 💸 Expense tracker 

A quick and easy to use expense tracking app to monitor personal finances and get a better idea of spending habits.

---

## 💡 Idea 

The idea to build an expense tracker came from a simple observation: my personal banking app didn't provide any easy way to visualize my spending habits over long periods of time. It only provided spending information over a period of 1 month, so I decided to create a tool to solve this issue.

--- 

## 📌 Features

- Filter spending by date
- View spending summaries over selected dates
- Pie charts to visualize spending categories
- Transactions table
- Responsive and user-friendly interface

--- 

## 🚀 Getting Started

### 📂 Structure 

The project is structured as follows:

```
spending_app/
├── data/
├── .gitignore
├── app.py
├── formatting.py
├── README.md
└── requirements.txt
```
The `data/` folder should contain all your transaction data. The format of the data is detailed below. Ensure you have all the required packages by running the command 

``pip install -r requirements.txt``

Then, you can run the app using the command

``streamlit run .\app.py``

The file `formatting.py` is used to put your data in the correct format if you are a BNP Paribas client (like me). Details are given below. The `test.ipynb`
### 🛠️ Data format

The app will run correctly only if your transaction data is in the right format. 

The data should be stored under  `data/transactions.xlsx`. It should include five columns, named `date`, `category`, `subcategory`, `label`, `amount`.

- `date` : date of the transaction
- `category` : type of expense/income (ex: everyday expense, banking, income, entertainment, etc.)
- `subcategory` : a more precise category (ex: travel, groceries, movies, savings, etc.)
- `label` : name of the transaction 
- `amount` : amount spent or received (positive or negative float)


The easiest way to get the data into this format for BNP Paribas users (like me) is to download the transaction data straight from your personal account, store it under `data/transactions.xls`, and run `formatting.py`. This will automatically save the data in the right format under `data/transactions.xlsx`. 

---

## 📧 Contact

- Name: Keenan Penner
- Email: keenan.penner@gmail.com   
- GitHub: https://github.com/Keenan-Penner





