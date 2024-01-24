import tkinter as tk
from tkinter import messagebox
from contact_manager import ContactManage, Contacts

"""
Label for displaying text.
Entry for user input.
Button for actions.
Listbox or Text for displaying a list or multi-line text.
Frame for grouping related widgets.

"""


class ContactGUI:

    def __init__(self):
        # Initialize instance attributes
        self.delete_button = None
        self.selected_contact_name = None
        self.contacts_listbox = None
        self.inner_email_frame = None
        self.inner_name_frame = None
        self.email_frame = None
        self.name_frame = None
        self.button_frame = None
        self.entry_frame = None
        self.modify_window = None
        self.exit_button = None
        self.modify_button = None
        self.view_button = None
        self.add_button = None
        self.email_label = None
        self.name_label = None
        self.main_label = None
        self.header_frame = None
        self.email_entry = None
        self.name_entry = None

        # Used for managing contacts
        self.manage = ContactManage()
        self.root = tk.Tk()

        self.root.title("Contact Management System")
        # User cannot change dimension of tk() window
        self.root.resizable(width=False, height=False)
        self.layout_setup()
        self.widget_setup()
        self.load_contacts_listbox_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.configure(background='cyan')
        self.root.mainloop()

    def layout_setup(self):
        # Call function and display app in the center
        self.center_window(600, 300)

    def widget_setup(self):
        # Color
        self.header_frame = tk.Frame(self.root, background='cyan')
        self.name_frame = tk.Frame(self.root, background='cyan')  # Frame for name label and entry
        self.email_frame = tk.Frame(self.root, background='cyan')  # Frame for email label and entry
        self.button_frame = tk.Frame(self.root, background='cyan')

        # Header Label
        self.main_label = tk.Label(self.header_frame, text="Contact Management", font=('Arial', 15), background='cyan')
        self.main_label.pack(side='top', pady=10)

        # Name Entry
        self.inner_name_frame = tk.Frame(self.name_frame, background='cyan')
        self.name_label = tk.Label(self.inner_name_frame, text="Name", font=('Arial', 12), background='cyan')
        self.name_label.pack(side='left')
        self.name_entry = tk.Entry(self.inner_name_frame, width=20)
        self.name_entry.pack(side='left', padx=10)
        self.inner_name_frame.pack(pady=5, padx=10, expand=True, fill='both', anchor='center')

        # Email Entry
        self.inner_email_frame = tk.Frame(self.email_frame, background='cyan')
        self.email_label = tk.Label(self.inner_email_frame, text="Email", font=('Arial', 12), background='cyan')
        self.email_label.pack(side='left')
        self.email_entry = tk.Entry(self.inner_email_frame, width=20)
        self.email_entry.pack(side='left', padx=10)
        self.inner_email_frame.pack(pady=5, padx=10, expand=True, fill='both', anchor='center')

        # Button Setup
        self.add_button = tk.Button(self.button_frame, text="Add Contact", command=self.add_contact,
                                    font=('Arial', 10), relief='groove')
        self.add_button.pack(side='left', padx=(40, 10), pady=10)

        self.view_button = tk.Button(self.button_frame, text="View Contact", command=self.view_contacts,
                                     font=('Arial', 10), relief='groove')
        self.view_button.pack(side='left', padx=10, pady=10)

        self.modify_button = tk.Button(self.button_frame, text="Modify Contact", command=self.modify_contacts,
                                       font=('Arial', 10), relief='groove')
        self.modify_button.pack(side='left', padx=10, pady=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit,
                                     font=('Arial', 10), relief='groove')
        self.exit_button.pack(side='left', padx=10, pady=10)

        # Packing Frames
        self.header_frame.pack(fill='x', padx=10, pady=10)
        self.name_frame.pack(fill='x', padx=200)
        self.email_frame.pack(fill='x', padx=200)
        self.button_frame.pack(fill='x', padx=10, pady=10)

        # Create a listbox to display contacts for modifying
        self.contacts_listbox = tk.Listbox(self.root, font=('Arial', 10), background='gray', borderwidth=5) # Fix me
        self.contacts_listbox.pack(side='left', fill='both', expand=True)
        self.contacts_listbox.bind("<<ListboxSelect>>", self.on_contact_select)

        # Add a scrollbar to listbox
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.contacts_listbox.yview)
        scrollbar.pack(side='left', fill='y')
        # Configure listbox to work with scrollbar
        self.contacts_listbox.config(yscrollcommand=scrollbar.set)

        # For contact deletion
        self.delete_button = tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact,
                                       font=('Arial', 10), relief='groove')
        self.delete_button.pack(side='left', padx=10, pady=10)

    def center_window(self, width, height):
        scr_width = self.root.winfo_screenwidth()
        scr_height = self.root.winfo_screenheight()
        # Half size display
        x = (scr_width // 2) - (width // 2)
        y = (scr_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def add_contact(self):
        name, email = self.name_entry.get(), self.email_entry.get()

        if name and email:
            if not self.manage.is_duplicate(name):
                self.manage.contacts[name] = Contacts(name, email)

                messagebox.showinfo("Success", f"{name} and {email} added successfully")
                # Save added contacts
                self.manage.save_to_json()
                # Refresh listbox with added contacts
                self.load_contacts_listbox_ui()
                # Delete entry after
                self.email_entry.delete(0, 'end')
                self.name_entry.delete(0, 'end')

            else:
                messagebox.showwarning("Warning", "Contact already exists")

        else:
            messagebox.showerror("Error", "Name or email cannot be empty")

    def view_contacts(self):
        contacts_info = "\n".join([self.manage.contacts[name].name_email() for name in sorted(self.manage.contacts)])
        messagebox.showinfo("Contacts", contacts_info if contacts_info else "No contacts available")
        # Delete the text entry after viewing the contacts
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')

    def on_contact_select(self, event):
        # Determine the widget that triggered the event
        widget = event.widget
        if len(widget.curselection()) > 0:
            index = int(widget.curselection()[0])
            selected_text = widget.get(index)
            self.selected_contact_name = selected_text.split(' - ')[0].strip(" ")
            # Load
            self.load_contact_details(self.selected_contact_name)

    def modify_contacts(self):
        # Get updated information from entry fields
        updated_name = self.name_entry.get()
        updated_email = self.email_entry.get()

        # Input validation
        if not updated_name or not updated_email:
            messagebox.showerror("Error", "Name or email cannot be empty")
            return

        if self.selected_contact_name in self.manage.contacts:
            # If name is changed, update contact manager
            if self.selected_contact_name != updated_name:
                # Remove old contact and add new one
                contact = self.manage.contacts.pop(self.selected_contact_name)
                contact.name = updated_name
                contact.email = updated_email
                self.manage.contacts[updated_name] = contact
            else:
                # Update email
                self.manage.contacts[updated_name].email = updated_email
            # Save updated contacts
            self.manage.save_to_json()
            # Refresh contact list in UI
            self.load_contacts_listbox_ui()
            # Clear input fields
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            messagebox.showinfo("success", "Contact updated successfully")
        else:
            messagebox.showerror("Error", "Contact does not exist")

    def load_contacts_listbox_ui(self):
        # Clear current contents of the Listbox
        self.contacts_listbox.delete(0, tk.END)

        # Populate the listbox with sorted contact names
        for contact_name in sorted(self.manage.contacts):
            contact = self.manage.contacts[contact_name]
            self.contacts_listbox.insert(tk.END, f" {contact.name} - {contact.email}")

    def load_contact_details(self, contact_name):
        # Retrieve contact details
        contact = self.manage.contacts.get(contact_name.strip(" ")) # Fix Me: Strip
        if contact:
            # Load the contact details into entry fields
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, contact.name)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contact.email)

    def update_contact(self):
        # Refresh the Listbox with updated contact list
        self.load_contacts_listbox_ui()

    def delete_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No contact selected")
            return

        contact_name = self.contacts_listbox.get(selected_index)
        if messagebox.askyesno("Confirm deletion", f"Are you sure you want to delete {contact_name.split(' - ')[0]}"):
            contact_name = contact_name.split(' - ')[0]
            if contact_name.strip(" ") in self.manage.contacts:
                del self.manage.contacts[contact_name.strip(" ")]

                self.manage.save_to_json()
                self.load_contacts_listbox_ui()
                messagebox.showinfo("Success", "Contact deleted successfully")
            else:
                messagebox.showerror("Error", "Contact does not exist")

    def exit(self):
        if messagebox.askyesno(title="Quit?", message="Are you sure you want to quit?"):
            self.root.destroy()
