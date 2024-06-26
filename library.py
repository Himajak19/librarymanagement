import tkinter as tk
from tkinter import ttk

class LibraryItem:
    def __init__(self, title, author, category, available):
        self.title = title
        self.author = author
        self.category = category
        self.available = available

class Library:
    def __init__(self):
        self.items = []
        self.checked_out = []
        self.fines = {}

    def add_item(self, item):
        self.items.append(item)

    def check_out(self, item, user):
        if item.available:
            item.available = False
            self.checked_out.append((item, user))
            print(f"{user} checked out {item.title}")
        else:
            print(f"{item.title} is not available")

    def return_item(self, item, user):
        if (item, user) in self.checked_out:
            item.available = True
            self.checked_out.remove((item, user))
            print(f"{user} returned {item.title}")
            self.calculate_fine(item, user)
        else:
            print(f"{user} did not check out {item.title}")

    def calculate_fine(self, item, user):
        # Calculate fine based on overdue days
        fine = 0
        if user in self.fines:
            fine = self.fines[user]
        self.fines[user] = fine + 10
        print(f"{user} owes a fine of ${self.fines[user]}")

    def search(self, title=None, author=None, category=None):
        results = []
        for item in self.items:
            if (title is None or title.lower() in item.title.lower()) and \
               (author is None or author.lower() in item.author.lower()) and \
               (category is None or category.lower() in item.category.lower()):
                results.append(item)
        return results

class LibraryGUI:
    def __init__(self, master):
        self.master = master
        master.title("Library Management System")

        self.library = Library()

        # Create the main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(padx=20, pady=20)

        # Create the search frame
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(pady=10)

        # Create the search widgets
        self.search_label = ttk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_items)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Create the item list
        self.item_list = ttk.Treeview(self.main_frame)
        self.item_list['columns'] = ('title', 'author', 'category', 'available')
        self.item_list.heading('#0', text='ID')
        self.item_list.heading('title', text='Title')
        self.item_list.heading('author', text='Author')
        self.item_list.heading('category', text='Category')
        self.item_list.heading('available', text='Available')
        self.item_list.pack(pady=10)

        # Create the action frame
        self.action_frame = ttk.Frame(self.main_frame)
        self.action_frame.pack(pady=10)

        self.check_out_button = ttk.Button(self.action_frame, text="Check Out", command=self.check_out_item)
        self.check_out_button.pack(side=tk.LEFT, padx=5)

        self.return_button = ttk.Button(self.action_frame, text="Return", command=self.return_item)
        self.return_button.pack(side=tk.LEFT, padx=5)

        self.add_button = ttk.Button(self.action_frame, text="Add Item", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Populate the item list
        self.populate_item_list()

    def populate_item_list(self):
        for item in self.library.items:
            self.item_list.insert('', 'end', text=str(self.library.items.index(item)), values=(item.title, item.author, item.category, item.available))

    def search_items(self):
        search_term = self.search_entry.get().lower()
        results = self.library.search(title=search_term, author=search_term, category=search_term)
        self.item_list.delete(*self.item_list.get_children())
        for item in results:
            self.item_list.insert('', 'end', text=str(self.library.items.index(item)), values=(item.title, item.author, item.category, item.available))

    def check_out_item(self):
        selected_item = self.item_list.focus()
        if selected_item:
            item_index = int(self.item_list.item(selected_item)['text'])
            item = self.library.items[item_index]
            self.library.check_out(item, "John")
            self.populate_item_list()

    def return_item(self):
        selected_item = self.item_list.focus()
        if selected_item:
            item_index = int(self.item_list.item(selected_item)['text'])
            item = self.library.items[item_index]
            self.library.return_item(item, "John")
            self.populate_item_list()

    def add_item(self):
        # Add code to create a new window for adding an item
        pass

root = tk.Tk()
library_gui = LibraryGUI(root)
root.mainloop()