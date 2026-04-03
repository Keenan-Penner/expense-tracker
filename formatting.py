import pandas as pd
import numpy as np

# I want to make separate data files for transactions each month
# I'll begin by importing the data with all transactions and putting it to the right format and cleaning the data

tester = pd.read_excel("data/transactions.xls",
                       skiprows= 2
)

# renaming columns
col_map = {'Date operation' : 'date',
           'Categorie operation' : 'category',
           'Sous Categorie operation' : 'subcategory',
           'Libelle operation' : 'label',
           'Montant operation' : 'amount',
           'Pointage operation' : 'status',
           'Commentaire operation' : 'comment'} 

tester = tester.rename(columns= col_map)

# removing useless columns and NaN rows
tester = tester.drop(columns= ['status', 'comment'])
tester = tester.dropna()

tester.to_excel("data/transactions.xlsx", index= False)

# setting date to datetime
tester['date'] = pd.to_datetime(tester['date'], format= "%d-%m-%Y")

for (year, month), group in tester.groupby([tester['date'].dt.year, tester['date'].dt.month]):
    filename = f"data/data_{year}_{month:02d}.xlsx"
    group.to_excel(filename, index= False)
