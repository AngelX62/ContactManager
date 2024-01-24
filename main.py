
import contact_manager
from contactGUI import ContactGUI
from contact_manager import ContactManage


def main():
    mode = input("Choose mode: (text/gui)\n")

    if mode == "text":
        # Instantiation to create an instance and access as method objects
        manage = ContactManage()
        replay = True
        while replay:
            try:
                menu = int(input("Menu: \n "
                                 "1) Add contact \n "
                                 "2) View contacts \n "
                                 "3) Modify contacts \n "
                                 "4) Exit\n".upper()))
            except ValueError:
                print("It must be a number")
                continue
            # Menu selection
            if menu == 1:
                manage.add_contact()
            elif menu == 2:
                manage.view_contacts()
            elif menu == 3:
                manage.modify_contacts()
            elif menu == 4:
                ex = contact_manager.exit_program()
                ex()
                break
    elif mode == "gui":
        ContactGUI()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
