import tkinter as tk
# from tkinter import messagebox
from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions


def send_query():
    query_type = query_type_var.get()
    query_text = query_text_box.get("1.0", tk.END).strip()
    server_address = server_address_var.get()

    # Perform the necessary operations with the query and server address

    with TypeDB.core_client(server_address) as client:  # Connect to TypeDB server
        print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as session
        print("\nRequest #1: Get query — User listing")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name $n;"
            response = transaction.query().match(typeql_read_query)  # Executing query
            # print(">TypeDB responded with", type(response), '<')  # Stream of ConceptMap
            k = 0
            for item in response:  # Iterating through response
                k += 1  # Counter
                print("User #" + str(k) + ": " + item.get("n").as_attribute().get_value())
            print("Users found:", k)  # Print number of results

    # Display the result in the output text field
    result_output.config(state=tk.NORMAL)
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, "Result goes here")
    result_output.config(state=tk.DISABLED)


def show_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    server_address_label = tk.Label(settings_window, text="Server address:")
    server_address_label.pack()

    server_address_entry = tk.Entry(settings_window, textvariable=server_address_var)
    server_address_entry.pack()

    save_button = tk.Button(settings_window, text="Save", command=settings_window.destroy)
    save_button.pack()


# Create the main window
root = tk.Tk()
root.title("GUI Application")

# Query type selector
query_type_label = tk.Label(root, text="Query type:")
query_type_label.grid(row=0, column=0, sticky="w")

query_type_var = tk.StringVar(root)
query_type_options = ["define", "undefine", "get", "insert", "delete", "update"]
query_type_selector = tk.OptionMenu(root, query_type_var, *query_type_options)
query_type_selector.config(width=10)
query_type_selector.grid(row=0, column=1, sticky="w")
query_type_var.set(query_type_options[0])

# Query text editor
query_text_label = tk.Label(root, text="Query:")
query_text_label.grid(row=1, column=0, sticky="w")

query_text_box = tk.Text(root, height=10, width=40)
query_text_box.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Result output
result_output_label = tk.Label(root, text="Result:")
result_output_label.grid(row=1, column=2, sticky="w")

result_output = tk.Text(root, height=10, width=40, state=tk.DISABLED)
result_output.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

# Send button
send_button = tk.Button(root, text="Send", command=send_query)
send_button.grid(row=3, column=0, padx=10, pady=10)

# Settings button
settings_button = tk.Button(root, text="Settings", command=show_settings)
settings_button.grid(row=0, column=3, padx=10, pady=10)

# Default server address
server_address_var = tk.StringVar(root, value="localhost:1729")

# Make GUI element sizes adjustable
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure((0, 1, 2), weight=1)

# Start the GUI event loop
root.mainloop()