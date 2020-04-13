class qBuilder:
    #Initializations

    def __init__(self):
        self.temp = True

    # 0 - Is your object BLANK?
    # 1 - Can your object BLANK?
    # 2 - Does your object BLANK?
    # 3 - Is your object a BLANK?
    # 4 - Does your object have BLANK?
    # 5 - Is your object related to BLANK?
    # 6 - Is your object a type of BLANK?
    # 7 - Can you BLANK your object?

    def getQuestion(self, char):
        question = ""
        qType = char.getQType()
        if(qType == 0):
            question = "Is your object "+char.get()+"?"
        elif(qType == 1):
            question = "Can your object "+char.get()+"?"
        elif(qType == 2):
            question = "Does your object "+char.get()+"?"
        elif(qType == 3):
            question = "Is your object a "+char.get()+"?"
        elif(qType == 4):
            question = "Does your object have "+char.get()+"?"
        elif(qType == 5):
            question = "Is your object related to "+char.get()+"?";
        elif(qType == 6):
            question = "Is your object a type of "+char.get()+"?";
        elif(qType == 7):
            question = "Can you "+char.get()+" your object?";
        else:
            question = "Does your object have the property of "+char.get()+""

        return question;
