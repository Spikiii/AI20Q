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
        if(qType in [0, 1, 2, 3, 4, 5, 6, 7]):
            if(qType == 0):
                question = "Is your object "+char.get()+"?"
            if(qType == 1):
                question = "Can your object "+char.get()+"?"
            if(qType == 2):
                question = "Does your object "+char.get()+"?"
            if(qType == 3):
                question = "Is your object a "+char.get()+"?"
            if(qType == 4):
                question = "Does your object have "+char.get()+"?"
            if(qType == 5):
                question = "Is your object related to "+char.get()+"?";
            if(qType == 6):
                question = "Is your object a type of "+char.get()+"?";
            if(qType == 7):
                question = "Can you "+char.get()+" your object?";
        else:
            question = "Does your object have the property of "+char.get()+""

        return question;
