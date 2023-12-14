import tkinter as tk
import pyodbc 
import openai
import config
import time
import re
import threading

openai.api_key = ""
print(f'openai.api_key : {openai.api_key}')

cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=MOHIT\SQLEXPRESS;"
                      "Database=QuestionBank;"
                      "Trusted_Connection=yes;")

def fetch(sub,diff):

        
    cursor=cnxn.cursor()
    query='select que from questions where topic=? AND difficulty=?'
    li=['Easy','Moderate','Hard']
    ans=[]
    if diff in li:
        if(diff=='Easy'):flag=1
        if(diff=='Moderate'):flag=2
        if(diff=='Hard'):flag=3
        print(sub)
        cursor.execute(query,(sub,flag))
        ans=cursor.fetchall()
        print("hello",ans)
    else:
        for i in range(0,3):
            cursor.execute(query,(sub,li[i]))
            ans.append(cursor.fetchall())
            cursor=cnxn.cursor()
    return ans


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
    cur= cnxn.cursor()
    topic=topic.lower()
    cur.execute("insert into Topic Values(?)",topic)
    cnxn.commit()
    for i in range(0,3):
        for j in range(0,3):
            query = 'generate a Questions bank on'+topic+' of difficulty '+dif[i]+'without answer'
            try:
                response = openAIQuery(query)
                li=[]
                #li=response.split('\n')
                pattern = r'\b\d+\..*?(?=\b\d+\.|$)'
                questions = re.findall(pattern,response, re.DOTALL)
                questions = [q.strip() for q in questions if q.strip()]
                for z in questions:
                    li.append(z)
                put(li,topic,i+1)
                time.sleep(15)
            #    print(f'Response : {response}')
            #    print(li)
            except Exception as e:
                print(f'Exception : {str(e)}')


def topiccheck(topic):
    cursor = cnxn.cursor()
    #program to check topic is available or not
    query='Select * from Topic where topic_name LIKE ?'
    cursor.execute(query,('%'+topic+'%'))
    row = cursor.fetchall()
    ans=[]
    for i in row:
        st=""
        for a in i:
            if(a!='(' or a!=')'):
                st+=a

        ans.append(st)
    return ans

difficulty=''
def submit(root, submit_button, TopicEntry, Diff_Var, output_entry, Diff_dropdown, TopicLabel, DiffLabel):
    topic = TopicEntry.get()
    difficulty = Diff_Var.get()

    if topic.strip() == "":
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(1.0, tk.END)
        output_entry.insert(tk.END, "Topic field is required!")
        output_entry.config(state=tk.DISABLED)
    else:
        # deleting current Window elements
        topic_list=["<<Generate New Or Train Data>>"]
        topic1_list=topiccheck(topic)
        topic_list.extend(topic1_list)
        print(topic_list,len(topic_list))
        if(len(topic_list)<=0):
            output_entry.config(state=tk.NORMAL)
            output_entry.delete(1.0, tk.END)
            output_entry.insert(tk.END, "Topic is not available")
            output_entry.config(state=tk.DISABLED)
        else:

            TopicLabel.grid_forget()
            TopicEntry.grid_forget()
            Diff_dropdown.grid_forget()
            DiffLabel.grid_forget()
            submit_button.grid_forget()

            # Adding new window elements
            TopicLabel_new = tk.Label(root, text="Select Topic :")
            TopicLabel_new.grid(row=0, column=1, padx=10, pady=10)

            Topic_Var = tk.StringVar()
            Topic_Var.set("Select topic")  # Default selection
            Topic_dropdown = tk.OptionMenu(root, Topic_Var, *topic_list)
            Topic_dropdown.grid(row=0, column=2, padx=10, pady=10)

            
            # Create submit button
            Get_button = tk.Button(root, text="get Questions")
            Get_button.grid(row=2, columnspan=2, padx=10, pady=10)
            Get_button.config( command= lambda: (getQuestion(topic, Topic_Var.get(), difficulty, output_entry)))
        


def getQuestion(top, topic, difficulty, output_entry):
    res=[]
    if(topic=="Select topic"):
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(1.0, tk.END)
        msg="please select the topic"
        output_entry.insert(tk.END, msg)
        output_entry.config(state=tk.DISABLED)
    else:
        print(topic, difficulty)
        
        if(topic=="<<Generate New Or Train Data>>"):
            output_entry.config(state=tk.NORMAL)
            output_entry.delete(1.0, tk.END)
            msg="Training the data......."
            output_entry.insert(tk.END, msg)
            output_entry.config(state=tk.DISABLED)
            thread = threading.Thread(target=train,args=(top,))
            thread.start()
          #  thread.join()
            # time.sleep(100)
            # res=fetch(topic,difficulty)
            # output_entry.config(state=tk.NORMAL)
            # output_entry.delete(1.0, tk.END)
            # for i in res:
            #     output_entry.insert(tk.END, i[0])
            # output_entry.config(state=tk.DISABLED)
        else:

            res=fetch(topic,difficulty)
            output_entry.config(state=tk.NORMAL)
            output_entry.delete(1.0, tk.END)
            for i in res:
                output_entry.insert(tk.END, i[0]+'\n\n')
            output_entry.config(state=tk.DISABLED)
        
        # Todo: add questions from database or find it from API

        # if(topic=='Generate New or Train Data'):
        #     # print('fetch data from API')
        # else:
        #     # print('fetch from database')

def main():
    # Create the main window
    root = tk.Tk()
    root.title("QBG")
    #root.iconbitmap('./icon.ico')

    # Set window size
    root.geometry("800x500")

    # Create labels and input fields
    TopicLabel = tk.Label(root, text="Topic:")
    TopicLabel.grid(row=0, column=1, padx=10, pady=10)

    TopicEntry = tk.Entry(root)
    TopicEntry.grid(row=0, column=2, padx=10, pady=10)

    DiffLabel = tk.Label(root, text="Difficulty:")
    DiffLabel.grid(row=1, column=1, padx=10, pady=10)

    # Options for difficulty selection
    Diff_Var = tk.StringVar()
    Diff_Var.set("Variable")  # Default selection
    Diff_options = ["Easy", "Moderate", "Hard", "Variable"] 
    Diff_dropdown = tk.OptionMenu(root, Diff_Var, *Diff_options)
    Diff_dropdown.grid(row=1, column=2, padx=10, pady=10)

    # Create output field
    output_entry = tk.Text(root, height=15, width=70, state=tk.DISABLED)
    output_entry.grid(row=3, column=2, columnspan=5, padx=10, pady=10)

    # Create submit button
    submit_button = tk.Button(root, text="Submit", command= lambda: (submit(root, submit_button, TopicEntry, Diff_Var, output_entry, Diff_dropdown, TopicLabel, DiffLabel)))
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

    # Run the main loop
    root.mainloop()


if __name__=='__main__':
   main()
# train('digital marketing')
