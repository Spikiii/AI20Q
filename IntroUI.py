def ui_screen():
    mode = input("What mode do you want to use? 'Game' or 'Data'\n") #figure out which user class this user is in
    if mode == "Game":
        input1 = input("Please enter your category: 'Animal', 'Plant', Mineral'\n") #determine
        if input1 == "Animal":
            # connect to Animal branch
        if input1 == "Plant":
            # connect to Plant branch
        if input1 == "Mineral":
            # connect to Mineral branch
    if mode == "Data":
        print("This feature isn't implemented yet, but it will be in the future.")

ui_screen()
