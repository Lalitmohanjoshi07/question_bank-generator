import tkinter as tk
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
        TopicLabel.grid_forget()
        TopicEntry.grid_forget()
        Diff_dropdown.grid_forget()
        DiffLabel.grid_forget()
        submit_button.grid_forget()

        # append the topics available in our database in the following list
        topic_list=['Generate New or Train Data']

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
        Get_button.config( command= lambda: (getQuestion(Topic_Var.get(), difficulty, output_entry)))
        

def getQuestion(topic, difficulty, output_entry):
    res=[]
    if(topic=="Select topic"):
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(1.0, tk.END)
        msg="please select the topic"
        output_entry.insert(tk.END, msg)
        output_entry.config(state=tk.DISABLED)
    else:
        print(topic, difficulty)
        res.append('hello')
        # Todo: add questions from database or find it from API

        # if(topic=='Generate New or Train Data'):
        #     # print('fetch data from API')
        # else:
        #     # print('fetch from database')

def main():
    # Create the main window
    root = tk.Tk()
    root.title("QBG")
    root.iconbitmap('./icon.ico')

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