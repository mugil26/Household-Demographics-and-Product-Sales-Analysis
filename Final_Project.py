import pandas as pd

#First, read in the transactions data.
df=pd.read_csv("./project_transactions.csv",usecols=['household_key', 'BASKET_ID', 'DAY', 'PRODUCT_ID', 'QUANTITY','SALES_VALUE'])

#Convert `DAY`, `QUANTITY`, and `PRODUCT_ID` to the smallest appropriate integer types.
df['DAY']=df['DAY'].astype('int32')
df['QUANTITY']=df['QUANTITY'].astype('int32')
df['PRODUCT_ID']=df['PRODUCT_ID'].astype('int32')
# print(df.info())

#Read in the `hh_demographic.csv` file, but only the columns `AGE_DESC`, `INCOME_DESC`, `household_key`, and `HH_COMP_DESC`. Convert the appropriate columns to the category dtype.
df1=pd.read_csv("./hh_demographic.csv",usecols=['AGE_DESC','INCOME_DESC', 'household_key','HH_COMP_DESC'])

df1['AGE_DESC']=df1['AGE_DESC'].astype('category')
df1['INCOME_DESC']=df1['INCOME_DESC'].astype('category')
df1['household_key']=df1['household_key'].astype('category')
df1['HH_COMP_DESC']=df1['HH_COMP_DESC'].astype('category')
# print(df1.info())

#Then group the transactions table by household_key, and calculate the sum of SALES VALUE by household.(use group_by method)
household_sales=df.groupby('household_key')['SALES_VALUE'].sum().reset_index()
# print(household_sales)

#Once you've done that, join the demographics DataFrame to the aggregated transactions table. Since we're interested in analyzing the demographic data we have, make sure not to include rows from transactions that don't match. (Inner join)
df_demo_trans=df.merge(df1,how='inner')
# print(df_analyis)

#Read in the product csv file
df2=pd.read_csv("./product.csv",usecols=['PRODUCT_ID','DEPARTMENT'])
# print(df2)

#Only read in product_id and department from product (consider converting columns).
print(df2.info())
df2['PRODUCT_ID']=df2['PRODUCT_ID'].astype('int32')
df2['DEPARTMENT']=df2['PRODUCT_ID'].astype('category')

#Join the product DataFrame to transactions and demographics tables, performing an inner join when joining both tables.
df_prod_trans=df2.merge(df,how='inner')
# print(df_prod_trans)
df_total_join=df_prod_trans.merge(df1,how='inner')
# print(df_total_join)

#Finally, pivot the fully joined dataframe by AGE_DESC and DEPARTMENT, calculating the sum of sales. Which category does our youngest demographic perform well in?
pivot_table=df_total_join.pivot_table(index='AGE_DESC',columns='DEPARTMENT',values='SALES_VALUE',aggfunc='sum')
print(pivot_table)

#Finally, export your pivot table to an excel file. Make sure to provide a sheet name.
pivot_table.to_excel("pivot_table.xlsx",sheet_name="My_data")