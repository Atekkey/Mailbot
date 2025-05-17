import regex as re

class personList:
    def __init__(self, fname = None):
        self.persons = []
        if(fname == None):
            return
        with open(fname, "r") as f: # read file
            for name in f:
                self.persons.append(name.strip().upper())
    
    def addName(self, str_name):
        self.persons.append(str_name.upper())
        self.persons.sort(key=len, reverse = True) # Sort by len, reverse
        # Runs here because its not at runtime

    def removeName(self, str_name):
        self.persons.remove(str_name)
    def printNames(self):
        print(self.persons)
    def getName(self, i):
        if(i < 0 or i >= len(self.persons)):
            return "Index out of bounds"
        return self.persons[i]
    def strCompare(self, str_name, strIn):
        score = 0
        print(re.search(str_name, strIn) != None)
        # TODO
        return score
    
    def strCompareToList1(self, longStr):
        for name in self.persons:
            if(re.search(name, longStr) != None):
                return name
        return ""
    
    def addIgnoreStr(self, strIn):
        self.ignoreList.append(strIn)
    def preproccess(self, longStr):
        longStr = longStr.upper()
        return longStr
        # strList = longStr.split(" ")
        # strListNew = []
        # for i in range(len(strList)):
        #     temp_str = strList[i]
        #     if(re.match(r"[0-9]*", temp_str) != None):
        #         strListNew.append(temp_str)
        
        # print(strList)
        # return