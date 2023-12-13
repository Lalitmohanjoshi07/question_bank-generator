import tkinter as tk

def submit(TopicEntry, Diff_Var, output_entry):
    topic = TopicEntry.get()
    difficulty = Diff_Var.get()

    if topic.strip() == "":
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(1.0, tk.END)
        output_entry.insert(tk.END, "Topic field is required!")
        output_entry.config(state=tk.DISABLED)
    else:
        output_entry.config(state=tk.NORMAL)
        output_entry.delete(1.0, tk.END)
        Questions=[]
        # Todo make API request and get data in array form in Questions array
        output_entry.insert(tk.END, f"Questions of topic {topic} with {difficulty} difficulty level:\n {Questions}")
        output_entry.config(state=tk.DISABLED)


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
    submit_button = tk.Button(root, text="Submit", command= lambda: (submit(TopicEntry, Diff_Var, output_entry)))
    submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

    # Run the main loop
    root.mainloop()


if __name__=='__main__':
    main()