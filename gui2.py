import tkinter as tk
# from tkinter import messagebox
from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions


def send_query():
    query_type = query_type_var.get()
    query_text = query_text_box.get("1.0", tk.END).strip()
    server_address = server_address_var.get()
    selected_database = database_var.get()

    # Perform the necessary operations with the query, server address, and selected database

    # Display the result in the output text field
    result_output.config(state=tk.NORMAL)
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, "Result goes here")
    result_output.config(state=tk.DISABLED)


def open_connection_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Connection Settings")

    server_address_label = tk.Label(settings_window, text="Server address:")
    server_address_label.pack()

    server_address_entry = tk.Entry(settings_window, textvariable=server_address_var)
    server_address_entry.pack()

    save_button = tk.Button(settings_window, text="Save", command=settings_window.destroy)
    save_button.pack()


def update_database_list(db_list_result):
    settings_window = tk.Toplevel(root)
    settings_window.title("Connection Settings")

    server_address_label = tk.Label(settings_window, text="Server address:")
    server_address_label.pack()

    server_address_entry = tk.Entry(settings_window, textvariable=server_address_var)
    server_address_entry.pack()

    save_button = tk.Button(settings_window, text="Update database list", command=settings_window.destroy)

    save_button.pack()

    with TypeDB.core_client(server_address_var.get()) as client:  # Connect to TypeDB server
        db_list = client.databases().all()
    db_list_result = [db.name() for db in db_list]
    return


# Create the main window
root = tk.Tk()
root.title("GUI Application")

# Connect button
connect_button = tk.Button(root, text="Connect...", command=open_connection_settings)
connect_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Query type selector
query_type_label = tk.Label(root, text="Query type:")
query_type_label.grid(row=0, column=2, sticky="e")

query_type_var = tk.StringVar(root)
query_type_options = ["define", "undefine", "get", "insert", "delete", "update"]
query_type_selector = tk.OptionMenu(root, query_type_var, *query_type_options)
query_type_selector.config(width=10)
query_type_selector.grid(row=0, column=3, sticky="e")
query_type_var.set(query_type_options[0])

# Database selector
database_var = tk.StringVar(root)
database_var.set("<Select database>")
database_selector = tk.OptionMenu(root, database_var, "<Select database>")
database_selector.config(width=15, state=tk.DISABLED)
database_selector.grid(row=0, column=1, padx=10, pady=10)
db_options = []
database_selector.bind("<Button-1>", lambda event: update_database_list(db_options))

database_selector = tk.OptionMenu(root, database_var, "<Select database>")

# Query text editor
query_text_label = tk.Label(root, text="Query:")
query_text_label.grid(row=1, column=0, sticky="w")

query_text_box = tk.Text(root, height=10, width=40)
query_text_box.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Result output
result_output_label = tk.Label(root, text="Result:")
result_output_label.grid(row=1, column=4, sticky="w")

result_output = tk.Text(root, height=10, width=40, state=tk.DISABLED)
result_output.grid(row=2, column=4, columnspan=4, padx=10, pady=10, sticky="nsew")

# Send button
send_button = tk.Button(root, text="Send", command=send_query)
send_button.grid(row=3, column=0, padx=10, pady=10)

# Make GUI element sizes adjustable
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure((0, 4), weight=1)

# Default server address
server_address_var = tk.StringVar(root, value="localhost:1729")

# Start the GUI event loop
root.mainloop()
