import bisect
import math


fuzzySetList = []
variableList = []
membership = None
membershipList = {}
outputMembershipList = {}
rulesList = []
crispValue = None
centroidList = {}
inputVarNameList = []
outputVarNameList = []
TRI = [0, 1, 0]
TRAP = [0, 1, 1, 0]
class fuzzyVariable:
    def __init__(self, varName, varType, range):
        self.varName = varName
        self.varType = varType
        self.range = range
        self.crispVal = crispValue
        self.fuzzySetList = fuzzySetList

class fuzzySet:
    def __init__(self, setName, setType, xList):
        self.setName = setName
        self.setType = setType
        self.xList = xList
        self.membership = membership

class fuzzyToolBox:
    def __init__(self, varList, rules):
        self.varList = varList
        self.rules = rules

    def fuzzification(self,variable, crispVal):
        # print("crispVal",crispVal)
        for set in variable.fuzzySetList:
            # crisp value outside limits
            if set.xList[0] > crispVal or set.xList[len(set.xList) - 1] < crispVal:
                set.membership = 0
                membershipList[set.setName] = set.membership
            # crisp value equal to coordinate
            elif crispVal in set.xList:
                index = set.xList.index(crispVal)
                countOccurance = set.xList.count(set.xList[index])
                if countOccurance > 1:
                    nextElementIndex = index + 1
                    if set.setType == "TRI":
                        val1 = TRI[index]
                        val2 = TRI[nextElementIndex]
                        set.membership = max(val1, val2)
                        membershipList[set.setName] = set.membership
                    elif set.setType == "TRAP":
                        val1 = TRAP[index]
                        val2 = TRAP[nextElementIndex]
                        set.membership = max(val1, val2)
                        membershipList[set.setName] = set.membership
                else:
                    if set.setType == "TRI":
                        set.membership = TRI[index]
                        membershipList[set.setName] = set.membership
                    elif set.setType == "TRAP":
                        set.membership = TRAP[index]
                        membershipList[set.setName] = set.membership
            elif set.xList[0] < crispVal and set.xList[len(set.xList) - 1] > crispVal:
                index = bisect.bisect_left(set.xList, crispVal)
                x1 = set.xList[index - 1]
                x2 = set.xList[index]
                y1 = 0
                y2 = 0
                if (set.setType == "TRI"):
                    y1 = TRI[index - 1]
                    y2 = TRI[index]
                if (set.setType == "TRAP"):
                    y1 = TRAP[index - 1]
                    y2 = TRAP[index]
                m = float(y2 - y1) / float(x2 - x1)
                c = y1 - (m * x1)
                set.membership = m * crispVal + c
                membershipList[set.setName] = set.membership

    def inference(self, rulesList, inputVarNameList, outputVarNameList):
        for rule in rulesList:
            temp = rule.rules
            rulesSplitted = temp.split()
            tempSetList = []

            for i in range(len(rulesSplitted)):
                if rulesSplitted[i] in inputVarNameList:
                    if rulesSplitted[i + 1] == "not" or rulesSplitted[i + 1] == "NOT" or rulesSplitted[i + 1] == "Not":
                        setMembershipVal = 1 - (membershipList[rulesSplitted[i + 2]])
                        tempSetList.append(setMembershipVal)
                    else:
                        setMembershipVal = membershipList[rulesSplitted[i + 1]]
                        tempSetList.append(setMembershipVal)
                elif rulesSplitted[i] == "and" or rulesSplitted[i] == "AND" or rulesSplitted[i] == "And":
                    tempSetList.append("and")

                elif rulesSplitted[i] == "or" or rulesSplitted[i] == "OR" or rulesSplitted[i] == "Or":
                    tempSetList.append("or")

                elif rulesSplitted[i] == "=>":
                    m = 0

                    while (m < len(tempSetList)):
                        if 'and' not in tempSetList:
                            break
                        if m < len(tempSetList) - 2:
                            if tempSetList[m + 1] == 'and':
                                Mini = min(tempSetList[m], tempSetList[m+ 2])
                                tempSetList[m + 2] = Mini
                                del tempSetList[m]
                                del tempSetList[m]
                                m = m
                            elif tempSetList[m + 1] == 'or':
                                if m < len(tempSetList) - 2:
                                    m =m + 2

                    maximum = tempSetList[0]
                    k = 0
                    while (k < len(tempSetList)):
                        if tempSetList[k] != 'or':
                            if tempSetList[k] > maximum:
                                maximum = tempSetList[k]
                        k = k + 1
                    if rulesSplitted[i + 1] in outputVarNameList:

                        if (outputMembershipList[rulesSplitted[i + 2]] != -1):
                            outputMembershipList[rulesSplitted[i + 2]] = max(
                                outputMembershipList[rulesSplitted[i + 2]], maximum)
                        else:
                            outputMembershipList[rulesSplitted[i + 2]] = maximum

    def deFuzzification(self):
        upperVal = 0
        resluts = []
        for var in variableList:
            if var.varType == "OUT" or var.varType == "out" or var.varType == "Out":
                for var2 in var.fuzzySetList:
                    temp = sum(var2.xList)
                    if var2.setType == "TRI":
                        centroidVal = temp / 3
                    else:
                        centroidVal = temp / 4
                    centroidList[var2.setName] = centroidVal
                    upperVal += centroidList[var2.setName] * outputMembershipList[var2.setName]
                if sum(outputMembershipList.values()) == 0:
                    print("can not divide by zero!")
                finalRes = upperVal / sum(outputMembershipList.values())
                res =  var.varName+ " is final Result " + str(finalRes)
                resluts.append(res)
                print(var.varName, " is final Result " , finalRes)
        return resluts



def variableIsExist(variableName, varList):
    for obj in varList:
        if obj.varName == variableName:
            return True



if __name__ == '__main__':
    toolflag = True
    menuFlag = True
    varFlage = True
    setFlag = True
    ruleFlag = True
    while toolflag == True:
        print("Fuzzy Logic Toolbox")
        print("===================")
        print("1- Create a new fuzzy system")
        print("2- Quit")
        toolInput = input()
        if toolInput == "1":
            print("1-Load my file")
            print("2-Enter manually")
            inp = input()
            if inp=='1':
                print("Enter the path")
                path = input()
                my_file = open(path, "r")
                innerText = my_file.read()
                text_list = innerText.split("\n")  # split with each new line
                text_list = [ele for ele in text_list if ele.strip()]  # Remove  empty spaces from the List
                # print("text_list awl",text_list)
                systemName = text_list[0]
                systemDiscrip = text_list[1]
                del text_list[0:2]

                """variable’s name, type (IN/OUT) and range ([lower, upper])"""
                numberOfvaribles = int(text_list[0])
                text_list.pop(0)
                varInput = []
                varInput_modfy = []
                for i in range(numberOfvaribles):
                    varInput.append(text_list[i])
                    ele = varInput[i].split(" ")
                    varInput_modfy.append(ele)
                    variableList.append(
                        fuzzyVariable(varInput_modfy[i][0], varInput_modfy[i][1], varInput_modfy[i][2]))
                del text_list[0:numberOfvaribles]

                """variable’s name
                    fuzzy set name, type (TRI/TRAP) and values """
                setInput = []
                setInput_modfy = []
                for i in range(numberOfvaribles):
                    variableName = text_list[0]
                    numFuzzysets = int(text_list[1])
                    del text_list[0:2]
                    for j in range(numFuzzysets):
                        setInput.append(text_list[j])
                        ele = setInput[j].split(" ")
                        setInput_modfy.append(ele)
                        res = [eval(i) for i in ele[2:]]
                        fuzzySetList.append(fuzzySet(setInput_modfy[j][0], setInput_modfy[j][1], res))
                    variableList[i].fuzzySetList = fuzzySetList
                    fuzzySetList = []
                    del text_list[0:numFuzzysets]
                    setInput = []
                    setInput_modfy = []

                """rules"""
                numRules = int(text_list[0])
                text_list.pop(0)
                for i in range(numRules):
                    rulesList.append(fuzzyToolBox(variableList, text_list[i]))

                del text_list[0:numRules]

                toolTemp = fuzzyToolBox(variableList, rulesList)
                temp = []
                for ele in text_list:
                    temp.append(ele.split())
                i = 0
                for variable in variableList:
                    if (variable.varType == "IN"):
                        variable.crispVal = int(temp[i][1])
                        i += 1
                        toolTemp.fuzzification(variable, variable.crispVal)
                        inputVarNameList.append(variable.varName)
                    elif variable.varType == "OUT":
                        outputVarNameList.append(variable.varName)
                        for x in variable.fuzzySetList:
                            outputMembershipList[x.setName] = -1


                toolTemp.inference(rulesList, inputVarNameList, outputVarNameList)

                reslist = toolTemp.deFuzzification()
                print("simulation is done.")
                f = open("output.txt", "w")
                f.write("System Name:\n")
                f.write(systemName)
                f.write("\n")
                f.write("Describtion:\n")
                f.write(systemDiscrip)
                f.write("\nfinal result:\n")
                f.write(str(reslist))
                f.close()

            elif inp =='2':
                print("Enter the system’s name and a brief description:")
                print("------------------------------------------------")
                sysInfo = input()
                breifInfo = input()
                while (menuFlag == True):
                    print("Main Menu:")
                    print("==========")
                    print("1- Add variables.")
                    print("2- Add fuzzy sets to an existing variable.")
                    print("3- Add rules.")
                    print("4- Run the simulation on crisp values.")
                    menuInput = input()
                    if menuInput == "1":
                        print("Enter the variable’s name, type (IN/OUT) and range ([lower, upper]):")
                        print("(Press x to finish)")
                        print("--------------------------------------------------------------------")
                        while (varFlage == True):
                            varInput = input().split()
                            if varInput[0] == "x" or varInput[0] == "X":
                                varFlage = False
                                break
                            elif len(varInput) < 3:
                                print("Data Is not Complete")
                                varFlage = False
                                break
                            else:
                                if (varInput[1] != 'IN' and varInput[1] != 'In' and varInput[1] != 'in' and
                                        varInput[1] != 'Out' and varInput[1] != 'OUT' and varInput[1] != 'out'):
                                    print("InValid Type")
                                else:
                                    variableList.append(fuzzyVariable(varInput[0], varInput[1], varInput[2]))
                        varFlage = True
                    elif menuInput == "2":
                        print("Enter the variable’s name:")
                        print("--------------------------")
                        variableName = input()
                        exist = variableIsExist(variableName, variableList)
                        if (exist == True):
                            print("Enter the fuzzy set name, type (TRI/TRAP) and values: (Press x to finish)")
                            print("-----------------------------------------------------")
                            while (setFlag == True):
                                setInput = input().split()

                                if setInput[0] == "x" or setInput[0] == "X":
                                    setFlag = False
                                    break
                                elif (len(setInput) < 3):
                                    print("INVALID INPUT")
                                    setFlag = False
                                    break
                                else:
                                    res = [eval(i) for i in setInput[2:]]
                                    fuzzySetList.append(fuzzySet(setInput[0], setInput[1], res))

                                    for obj in variableList:
                                        if obj.varName == variableName:
                                            obj.fuzzySetList = fuzzySetList
                            fuzzySetList = []
                            setFlag = True
                        else:
                            print("Variable Is Not Exist")
                    elif (menuInput == "3"):
                        if (len(variableList) != 0):
                            print("Enter the rules in this format: (Press x to finish)")
                            print("IN_variable set operator IN_variable set => OUT_variable set")
                            print("------------------------------------------------------------")
                            while (ruleFlag == True):
                                rulesInput = input()
                                if (rulesInput == "x" or rulesInput == "X"):
                                    ruleFlag = False
                                    break
                                else:
                                    rulesList.append(fuzzyToolBox(variableList, rulesInput))
                    elif (menuInput == "4"):
                        if (len(rulesList) == 0 and len(fuzzySetList) == 0):
                            print("CAN’T START THE SIMULATION! Please add the fuzzy sets and rules first.")
                        else:
                            inputVarNameList = []
                            outputVarNameList = []
                            toolTemp = fuzzyToolBox(variableList, rulesList)
                            print("Enter the crisp values:")
                            print("-----------------------")
                            for variable in variableList:
                                if (
                                        variable.varType == "IN" or variable.varType == "in" or variable.varType == "In"):
                                    print(variable.varName, ":")
                                    crispInput = int(input())
                                    variable.crispVal = crispInput
                                    toolTemp.fuzzification(variable, variable.crispVal)
                                    inputVarNameList.append(variable.varName)
                                elif variable.varType == "OUT" or variable.varType == "out" or variable.varType == "Out":
                                    outputVarNameList.append(variable.varName)
                                    for x in variable.fuzzySetList:
                                        outputMembershipList[x.setName] = -1
                            print("Fuzzification ==> Done")
                            toolTemp.inference(rulesList, inputVarNameList, outputVarNameList)
                            print("Infernce ==> Done")
                            # print(outputMembershipList)
                            print("Defuzzification ==> Done")
                            res=toolTemp.deFuzzification()

                    elif (menuInput == "Close" or menuInput == "close"):
                        menuFlag = False
                        break
                else:
                    break
        elif (toolInput == "2"):
            toolflag = False
            break
        else:
            print("Invalid Answer!! Try Again")



