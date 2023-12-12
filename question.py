import pyodbc 
cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=LALIT\SQLEXPRESS;"
                      "Database=QuestionBank;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()
#program to check topic is available or not
searchtopic=input("Enter the topic")
query='Select * from Topic where topic_name LIKE ?'
cursor.execute(query,('%'+searchtopic+'%'))
row = cursor.fetchall()

# Check if the row fetched is not None (indicating data was fetched)
if row is not None:
    print("Data fetched successfully.")
    print(row)
else:
    print("No data fetched.")