import gameState

def ui_screen():
    mode = input("What mode do you want to use? 'Game' or 'Data'\n") #figure out which user class this user is in
    if mode == "Data":
        print("This feature isn't implemented yet, but it will be in the future.")
    if mode == "Game":
        input1 = input("Please enter your category: 'Animal', 'Plant', Mineral'\n") #determine
        if input1 == "Animal":
            # connect to Animal branch
        if input1 == "Plant":
            # connect to Plant branch
        if input1 == "Mineral":
            # connect to Mineral branch


ui_screen()
game = gameState(input1) #keeps track of the game's state
questions = 0 #keeps track of number of questions asked
playing = true #keeps track of whether the player is still playing
picker = cPicker()
builder = qBuilder()       
while(playing):
    questions++ # increment questions
    char = picker.getChar(gameState) #get the characteristic to check about this round
    ans = input(builder.getQuestion(char) + "y/n\n") #builds a question and asks the user
    if ans == "y": #set the truth value of the  characteristic
        char.setTruth(True)
    if ans == "n":
        char.setTruth(False)
    game.addChar(char) #update the gamestate

    ## TODO: guess if we have a high enough confidence value

    if questions = 20:
        playing = false
print("Thank you for playing!")
