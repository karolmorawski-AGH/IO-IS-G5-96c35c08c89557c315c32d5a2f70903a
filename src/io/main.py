import sys
import graph_sketcher as gs

directory = "./"
if len(sys.argv) > 1:
    directory = sys.argv[1]

# Creating drawer class which contains methods used below in the dynamic menu
graphSketcher = gs.DrawGraph(directory)

# menu
exit_condition = '0'
choice = '0'
while exit_condition == '0':
    print('\033[2J')  # Clear screen
    print("___________________________________________________________")
    print("\t     Dynamic menu for graph drawing")
    print("___________________________________________________________\n")

    print("Chosen directory: " + directory + "\n")

    # 1
    print("[1]:\tDraw\t", end="")
    print("\033[1;32;33mFILE" + '\033[0m', end="")
    print("\t\t\t\t\trelationship diagram")
    # 2
    print("[2]:\tDraw\t", end="")
    print("\033[1;32;96mMETHOD" + '\033[0m', end="")
    print("\t\t\t\t\trelationship diagram")
    # 3
    print("[3]:\tDraw\t", end="")
    print("\033[1;35;35mMODULE" + '\033[0m', end="")
    print("\t\t\t\t\trelationship diagram")
    # 4
    print("[4]:\tDraw\t", end="")
    print("\033[1;32;33mFILE" + '\033[0m', end=" ")
    print("+ " + "\033[1;32;96mMETHOD" + '\033[0m', end="")
    print("\t\t\trelationship diagram")
    # 5
    print("[5]:\tDraw\t", end="")
    print("\033[1;32;33mFILE" + '\033[0m', end=" ")
    print("+ " + "\033[1;32;35mMODULE" + '\033[0m', end="")
    print("\t\t\trelationship diagram")
    # 6
    print("[6]:\tDraw\t", end="")
    print("\033[1;32;96mMETHOD" + '\033[0m', end=" ")
    print("+ " + "\033[1;32;35mMODULE" + '\033[0m', end="")
    print("\t\t\trelationship diagram")
    # 7
    print("[7]:\tDraw\t", end="")
    print("\033[1;32;33mFILE" + '\033[0m', end=" ")
    print("+ " + "\033[1;32;96mMETHOD" + '\033[0m', end=" ")
    print("+ " + "\033[1;32;35mMODULE" + '\033[0m', end="")
    print("\trelationship diagram")
    # Exit
    print("Type q to exit the program")

    choice = input("\n:")

    if choice == "1":
        print("\nGraph generated")
        graphSketcher.draw_file_graph()
        input("Press enter to continue...")
    elif choice == "2":
        print("\nGraph generated")
        input("Press enter to continue...")
        graphSketcher.draw_method_graph()
    elif choice == "3":
        print("\nGraph generated")
        graphSketcher.draw_module_graph()
        input("Press enter to continue...")
    elif choice == "4":
        print("\nGraph generated")
        input("Press enter to continue...")
    elif choice == "5":
        print("\nGraph generated")
        input("Press enter to continue...")
    elif choice == "6":
        print("\nGraph generated")
        input("Press enter to continue...")
    elif choice == "7":
        print("\nGraph generated")
        input("Press enter to continue...")
    elif choice == "q":
        exit(0)
    else:
        input("\nWrong input.\nPress enter to continue...")
