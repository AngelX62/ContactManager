from contactGUI import ContactGUI
from contact_manager import ContactManage, exit_program


class Main:

    def __init__(self):
        # Instantiation to create an instance and access as method objects
        self.manage = ContactManage()

    def menu(self):
        mode = input("Choose mode: (text/gui)\n").lower()

        if mode == "text":
            while True:
                try:
                    options = int(input("Menu: \n "
                                        "1) Add contact \n "
                                        "2) View contacts \n "
                                        "3) Modify contacts \n "
                                        "4) Exit\n".upper()))
                except ValueError:
                    print("It must be a number")
                    continue
                # Menu selection
                if options == 1:
                    self.manage.add_contact()
                elif options == 2:
                    self.manage.view_contacts()
                elif options == 3:
                    self.manage.modify_contacts()
                elif options == 4:
                    exit_program()
                    break
        elif mode == "gui":
            ContactGUI()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main = Main()
    main.menu()
