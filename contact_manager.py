import json


class Contacts:
    # Constructor method and initialize instance emails
    def __init__(self, name, email):
        self.name = name
        self.email = email

    # Instance methods within a class
    # Return formatted string with contact's name and email
    def name_email(self):
        return f"{self.name} | {self.email}"

    # Convert contact object to dictionary format
    def to_dict(self):
        return {'Name': self.name, 'Email': self.email}

    # Class method to create a Contacts object from a dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(data['Name'], data['Email'])


# Function to print exit message
def exit_program():
    print("Thank you for using our service, goodbye!")


class ContactManage:
    # Initialize ContactManage with empty contacts dictionary and load contacts from JSON
    def __init__(self):
        self.contacts = {}
        self.load_from_json()

    # Determine if given name already exists in the list
    def is_duplicate(self, name):
        return name in self.contacts

    # Save current contacts to a JSON file
    def save_to_json(self):
        # Sort contacts and convert each contact object to dictionary format
        sort_contacts = dict(sorted(self.contacts.items(), reverse=False))
        contact_dict = {"Contacts": {name: contacts.to_dict() for name, contacts in sort_contacts.items()}}

        # Write the contacts dictionary to a JSON file
        with open("contacts.json", "w") as file:
            json.dump(contact_dict, file, indent=4)

    # Load contacts from a JSON file
    def load_from_json(self):
        try:
            with open("contacts.json", "r") as file:
                entire_dict = json.load(file)
                contacts_data = entire_dict.get("Contacts", {})

                # Convert each contact in the JSON file to a Contacts object
                if isinstance(contacts_data, dict):
                    self.contacts = {name: Contacts.from_dict(data) for name, data in contacts_data.items()}
                else:
                    print("Unexpected data format in JSON file.")
        except (FileNotFoundError, json.JSONDecodeError):
            self.contacts = {}

    # Add new contacts to the contact list
    def add_contact(self):
        is_valid_input = False

        while not is_valid_input:
            try:
                # Add specified number of new contacts to the contacts list
                add_num_contacts = int(input("Enter the amount of contacts you want to add: "))
                break

            except ValueError:
                print("It must be a number: ")

        for i in range(add_num_contacts):
            while True:
                # Get contact's name and email
                name = input(f"Enter the name of contact {i + 1}: ").capitalize()

                # Check if entered name already exists
                if not self.is_duplicate(name):
                    email = input("Enter {}'s email: ".format(name))
                    if "@" in email:
                        self.contacts[name] = Contacts(name, email)
                        # Exit loop after adding a non-duplicate name
                        break
                    else:
                        print("It must be an email")
                # Prints and loops again
                else:
                    print(f"The name {name} already exists, please enter a different name:")
            # Save the updated contacts list to JSON file
            self.save_to_json()

    # Display all the contacts
    def view_contacts(self):
        # Executes if there are values in the contact list
        if self.contacts:
            print("Here are your contacts: \n")
            sort_names = sorted(self.contacts.keys())
            # Join the contact info into one single string
            # map applies the function and then yields the result for that item.
            # The returned map object can be converted into a list or other iterable types for further use or iteration.
            # Used lambda (anonymous function)
            print("\n".join(map(lambda name: self.contacts[name].name_email(), sort_names)))
        else:
            print("No contacts available")

    # Modify existing contacts
    def modify_contacts(self):
        # Runs view_contacts method
        self.view_contacts()

        try:
            modify_name = input("Enter the contact name you want to modify:\n").capitalize()
            if modify_name in self.contacts:
                # contacts_key = list(sorted(self.contacts))
                remove_options = int(input("Select the choices:\n"
                                           "1. Delete contact\n"
                                           "2. Edit contact name\n"
                                           "3. Edit contact email\n"))

                if remove_options == 1:
                    self.delete_contacts(modify_name)
                elif remove_options == 2:
                    self.edit_name(modify_name)
                elif remove_options == 3:
                    self.edit_email(modify_name)
                else:
                    print("Invalid option, try again")
            else:
                print("Invalid Contact name")
        except ValueError:
            print("Please enter a number")

    def delete_contacts(self, name):
        # self.contacts.pop(name)
        del self.contacts[name]
        print(f"Success! {name} has been deleted.")
        self.save_to_json()

    def edit_name(self, name):
        new_name = input("Enter the new name:").capitalize()

        while True:
            if new_name in self.contacts and new_name == name:
                print("The name already exist, type a different name")
                new_name = input().capitalize()
            # Rename contact: Remove old name entry and reassign email to the new name
            contact = self.contacts.pop(name)
            # Update name email of the contacts object
            contact.name = new_name
            self.contacts[new_name] = contact
            print(f"You have changed the name to {new_name}")

            self.save_to_json()
            break

    def edit_email(self, name):
        new_email = input("Enter the new email:")

        if new_email.__contains__("@"):
            self.contacts[name].email = new_email
            print(f"{name}'s email has been changed to {new_email}")
            self.save_to_json()
        else:
            print("It must be an email")

