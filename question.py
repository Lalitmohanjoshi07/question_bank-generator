import pyodbc 
import openai
import config
import time

openai.api_key = "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"
print(f'openai.api_key : {openai.api_key}')

cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=MOHIT\SQLEXPRESS;"
                      "Database=QuestionBank;"
                      "Trusted_Connection=yes;")

def fetch(sub,diff):
    cursor=cnxn.cursor()
    query='select * from questions where topic=? AND difficulty=?'
    cursor.execute(query,(sub,diff))
    row=cursor.fetchall()
    for row in row:
        print(row)


def put(quest,sub,diff):
    cursor=cnxn.cursor()
    query='insert into questions values(?,?,?)'
    for row in quest:
        if(len(row)>0):
            cursor.execute(query,(row,sub,diff))
    cnxn.commit()


def openAIQuery(query):
    response = openai.Completion.create(
      engine="davinci-instruct-beta-v3",
      prompt=query,
      temperature=0.8,
      max_tokens=500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0)

    if 'choices' in response:
        if len(response['choices']) > 0:
            answer = response['choices'][0]['text']
        else:
            answer = 'Opps sorry, you beat the AI this time'
    else:
        answer = 'Opps sorry, you beat the AI this time'

    return answer

def train(topic):
    if not openai.api_key:
        print(f'api_key is not set')
        exit(0)
    dif=['Easy','Medium','Hard']
    
    for i in range(0,3):
        for j in range(0,3):
            query = 'generate a Questions bank on'+topic+' of difficulty '+dif[i]+'without answer and put #@# in the end of every question'
            try:
                response = openAIQuery(query)
                li=[]
                li=response.split('\#@#');
                put(li,topic,i+1)
                time.sleep(15)
                print(f'Response : {response}')
                print(li)
            except Exception as e:
                print(f'Exception : {str(e)}')





train('java')
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




















































    