class Contacts:
    # Constructor method and initialize instance attributes
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

    # Instance methods within a class
    def name_attribute(self):
        return f"Name: {self.name} | Attribute: {self.attribute}"


def exit_program():
    print("Thank you for using our service, goodbye!")


class ContactManage:

    def __init__(self):
        self.contacts = {}

    def is_duplicate(self, name):
        # Determine if given name already exists in the list
        return name in self.contacts

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
                # Input name
                name = input(f"Enter the name of contact {i + 1}: ").capitalize()

                # Check if entered name already exists
                if not self.is_duplicate(name):
                    attribute = input("Describe {} in one word: ".format(name))
                    self.contacts[name] = Contacts(name, attribute)
                    # Exit loop after adding a non-duplicate name
                    break
                # Prints and loops again
                else:
                    print(f"The name {name} already exists, please enter a different name:")

    def view_contacts(self):
        # Executes if there are values in the contact list
        if self.contacts:
            print("Here are your contacts: \n")
            sort_names = sorted(self.contacts.keys())

            for name in sort_names:
                print(self.contacts[name].name_attribute())
        else:
            print("No contacts available")

    def remove_contacts(self):
        # If user does not enter any contacts
        if len(self.contacts) == 0:
            print("You do not have any existing contacts\n")

        else:
            # second object (contact_dict) is used to capture the value from the iterable.
            # Enumerate function retrieves both the index and element value. It
            # captures index, contact_dict captures the value
            sorted_contacts = sorted(self.contacts.keys())
            for i, contact_dict in enumerate(sorted_contacts):
                print(f"(Contact {i + 1})", "{}".format(self.contacts[contact_dict].name_attribute()))

            while True:
                try:
                    # Subtract 1 to get the right index to delete contact
                    delete_contact_index = int(input("\nEnter the number (s) of contact you want to delete: ")) - 1

                    if 0 <= delete_contact_index <= len(self.contacts):
                        remove_key = list(self.contacts.keys())[delete_contact_index]
                        self.contacts.pop(remove_key)
                        print("Success! contact:", delete_contact_index + 1, "has been deleted.")
                        break
                    else:
                        print("Invalid input")

                except ValueError:
                    print("Must be a number:")


# Main method outside the two classes
def main():
    # Instantiation to create an instance and access as method objects
    manage = ContactManage()
    replay = True
    while replay:
        try:
            menu = int(input("Menu: \n 1) Add contact \n 2) View contacts \n 3) Remove contacts \n 4) Exit\n".upper()))
        except ValueError:
            print("It must be a number")
            continue
        # Menu selection
        if menu == 1:
            manage.add_contact()
        elif menu == 2:
            manage.view_contacts()
        elif menu == 3:
            manage.remove_contacts()
        elif menu == 4:
            exit_program()
            break


# Run program
if __name__ == "__main__":
    main()
