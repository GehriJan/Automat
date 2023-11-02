from classes import *
from globalStuff import *


def renameStates(auto: Automat, index: int) -> Automat:
    newStates: set = set()
    
    if(index<=auto.states.__len__()):
        auto = renameStates(auto, auto.states.__len__()+1)
    
    
    # Für alle Zustände:
    for state in auto.states:
        
        # Neuer Startzustand
        if state == auto.startState:
            auto.startState = index
        # Neue Relationen hinzufügen
        for change in auto.relation:
            tempList = list(change)

            if tempList[0] == state:
                tempList[0] = index
            if tempList[2] == state:
                tempList[2] = index
                
            auto.relation.remove(change)    
            auto.relation.add(tuple(tempList))
        # Neue Endzustände
        for endState in auto.endStates:
            if state == endState:
                auto.endStates.discard(state)
                auto.endStates.add(index)
                break
        # Ändere Vorkommen in Zuständen
        newStates.add(index)

        index = index + 1
    auto.states = newStates
    return auto

def concatNEA(autoOne: Automat, autoTwo: Automat) -> Automat:
    autoOut = NEA()
    
    #Indizes anpassen
    autoOne = renameStates(autoOne, 0)
    autoTwo = renameStates(autoTwo, autoOne.states.__len__())

    #Neuen Automaten bauen
    autoOut.alphabet = autoOne.alphabet.union(autoTwo.alphabet)
    autoOut.states = autoOne.states.union(autoTwo.states)
    autoOut.relation = autoOne.relation.union(autoTwo.relation)
    
    #Spezielle Start-End-Anpassungen
    autoOut.startState = autoOne.startState
    autoOut.endStates = autoTwo.endStates
    
    #Epsilonverbindungen machen    
    for endAutoOne in autoOne.endStates:
        autoOut.relation.add((endAutoOne, eps, autoTwo.startState))
    
    return autoOut

def unionNEA(autoOne: Automat, autoTwo: Automat) -> Automat:
    autoOut = NEA()
    #Indizes anpassen
    autoOne = renameStates(autoOne, 1)
    autoTwo = renameStates(autoTwo, 1+autoOne.states.__len__())
    
    #Neuen Automaten bauen
    autoOut.startState = 0
    autoOut.states = autoOne.states.union(autoTwo.states)
    autoOut.states.add(0)
    autoOut.alphabet = autoOne.alphabet.union(autoTwo.alphabet) # todo: wird das alphabet geunioned oder muss das definitionsgemäß gleich sein?
    autoOut.relation = autoOne.relation.union(autoTwo.relation)
    autoOut.relation.add(tuple((0, eps, autoOne.startState)))
    autoOut.relation.add(tuple((0, eps, autoTwo.startState)))
    autoOut.endStates = autoOne.endStates.union(autoTwo.endStates)
    
    return autoOut

def kleeneNEA(auto: Automat) -> Automat:
    
    auto = renameStates(auto, 1)
    
    auto.states.add(0)
    auto.relation.add(tuple((0, eps, auto.startState)))
    auto.startState = 0
    for endState in auto.endStates:
        auto.relation.add(tuple((endState, eps, 0)))
    auto.endStates.clear()
    auto.endStates.add(0)
    
    return auto

def reg2nea(reg: str) -> Automat:
    
    reg = addBrackets(reg)
    
    return inputString2nea(reg)

def inputString2nea(inputString: str) -> Automat:
    autoOut: NEA
    # Annahme: Der String ist perfekt geklammert, niemals befinden sich zwei Operanden direkt in derselben Klammer
    operationName = str()
    operation: dict ={
        "concat": concatNEA,
        "union": unionNEA
    }
    
    inputString = inputString.strip()

    
    inputString = inputString[1:-1] #Problem: ein Automat wie ((a)) schafft es hier durch, und wird dann zu (a). Da denkt das Programm, dass es einen Operator gibt und wird lost
    # Atomare Automaten
    if(len(inputString)==1):
        autoOut = SingleCharNEA(inputString)
        return autoOut
    
    # Kleene bestimmen
    if(inputString[-1]=='*'):
        return kleeneNEA(inputString2nea(inputString[:-1]))
    
    # Position union/concat
     
    posOperation: int = countBrackets(inputString).index(0)+1
    
    # Operation bestimmen
    if inputString[posOperation:posOperation+1]=='+':
        operationName = "union"
    else:
        operationName = "concat"
    
    # Operanden bestimmen

    operandOne: str = inputString[:posOperation]
    operandTwo: str = inputString[posOperation+1:]
    
    autoOne = inputString2nea(operandOne)
    autoTwo = inputString2nea(operandTwo)
    
    autoOut = operation[operationName](autoOne, autoTwo)
    
    return autoOut

def countBrackets(input: str) -> list:
    # outputs a list of numbers indicating the number of opened bracket
    # "environments" to the specific index (including the index)
    stringList: list = list(input)
    counter: int = 0

    for i in range(len(input)):
        if stringList[i]=='(':
            counter += 1
        if stringList[i]==')':
            counter -= 1
        stringList[i]=counter
    
    return stringList

def addBrackets(inputString: str) -> str:

    inputString = inputString.strip()
    # encapsulate letters
    alphabet: set = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
    for letter in alphabet:
        inputString = inputString.replace(letter, f"({letter})")
    
    #Kleenes klammern
    inputString = encapsKleene(inputString)

    #Concat Klammern
    inputString = inputString.replace(")(", f").(")
    inputString = encapsOperation(inputString, ".")
    
    #Union Klammern
    inputString = encapsOperation(inputString, "+")
    
    return f"({inputString})"

def encapsKleene(inputString: str) -> str:
    # ENCAPSULATE KLEENES
    # pseudo code:
    #   nächsten Kleene finden
    #   positionen (links und rechts) finden
    #   neuen String zusammenbasteln

    posStar = inputString.rfind("*")
    while not posStar==-1:
        
        bracketList: list = countBrackets(inputString[:posStar])
        depthStar = bracketList[posStar-1]
        
        # find positions
        rIndex = posStar
        lIndex = rindex(bracketList[:posStar-1], depthStar)
        
        # build new String
        leftOuterStr = inputString[:lIndex+1]
        innerStr = inputString[lIndex+1:rIndex+1]
        rightOuterStr = inputString[rIndex+1:]
        
        inputString = f"{leftOuterStr}({innerStr}){rightOuterStr}"
        posStar = inputString[:posStar+1].rfind("*")
        
    return inputString

def encapsOperationPrev(inputString: str, operation: str) -> str:
    
    # PSEUDO CODE
    # Erstelle bracketList
    # Trage Ops mit Tiefe ein
    # Von höchster bis niedrigster:
    #   Finde Rechte und LInke Position
    #   Klammere Ausdruck
    #   Passe
    
    # Erstelle Brakcetlists
    bracketList: list = countBrackets(inputString)
    concatOperators = dict()
    index = 0
    
    # Find Operation and add to dict (including depth)
    for symbol in inputString:
        if symbol==".":
            concatOperators[index] = bracketList[index]
        index += 1
        
    # sort dictionary
    concatOperators = sortDict(concatOperators)

    # from highest to lowest
    for operator in concatOperators:
        
        depthOperator = concatOperators[operator]
        
        #determine right and left Position
        rIndex = bracketList[operator+1:].index(depthOperator) + operator
        lIndex = rindex(bracketList[:operator-1], depthOperator)
        
        # build new String
        leftOuterStr = inputString[:lIndex+1]
        innerStr = inputString[lIndex+1:rIndex+1]
        rightOuterStr = inputString[rIndex+1:]
        
        if not (leftOuterStr.endswith("(") and rightOuterStr.startswith(")")): # in diesem Fall ist die Klammer unnötig, weil sie quasi doppelt da stehen würe
            inputString = f"{leftOuterStr}({innerStr}){rightOuterStr}"
            for operator in concatOperators:
                if operator > rIndex:
                    concatOperators[operator+2] = concatOperators.pop(operator)
                    continue
                if operator > lIndex:
                    concatOperators[operator+1] = concatOperators.pop(operator)
                    continue
            concatOperators = sortDict(concatOperators)
            
            

        
        # Problem: der erste Concat ist wahrscheinlich richtig behandelt, aber die Indizes im Dict haben sich geänder    
    
    return "hello"

def encapsOperation(inputString: str, operation: str) -> str:
    
    # PSEUDO CODE
    # Erstelle bracketList
    # Trage Ops mit Tiefe ein
    # Von oben bis unten
    #   Finde Rechte und LInke Position
    #   Klammern Passen? -> bis zum ersten, wos nicht passt
    #   Klammern
    #   Funktion auf neuem String aufrufen
    # (((((a).((b)*)).((((a)+(b)))*)).(c)).(a))
    # der Code soll quasi pro Rekursion die tiefste Multiplikation verklammern und, wenn es keine mehr gibt, den fertigen String zurückgeben
    
    # Erstelle Brakcetlists
    bracketList: list = countBrackets(inputString)
    concatOperators = dict()
    index = 0
    
    # Find Operation and add to dict (including depth)
    for symbol in inputString:
        if symbol==".":
            concatOperators[index] = bracketList[index]
        index += 1
        
    # sort dictionary
    concatOperators = sortDict(concatOperators)

    # from highest to lowest
    for operator in concatOperators:
        
        depthOperator = concatOperators[operator]
        
        #determine right and left Position
        rIndex = bracketList[operator+1:].index(depthOperator) + operator + 2
        lIndex = rindex(bracketList[:operator-1], depthOperator) + 1
        
        # build new String
        leftOuterStr = inputString[:lIndex]
        innerStr = inputString[lIndex:rIndex]
        rightOuterStr = inputString[rIndex:]
        
        if leftOuterStr.endswith("(") and rightOuterStr.startswith(")"): # in diesem Fall ist die Klammer unnötig, weil sie quasi doppelt da stehen würe
            continue
        else:
            inputString = f"{leftOuterStr}({innerStr}){rightOuterStr}"
            return encapsOperation(inputString, operation)
        
    return inputString
            


def sortDict(input: dict) -> dict:
    return dict(sorted(input.items(), key=lambda item: item[1], reverse=True))

def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

# print(inputStringAddBrackets("((a)((a+b))*ca)"))
print(addBrackets("((ab*)((a+b))*ca)" + "\n"))
print(addBrackets("a+b" + "\n"))
print(addBrackets("(ab*)+bc" + "\n"))
# print(inputStringAddBrackets("((ab*)((a+(bb)(ab(ba)*a)))*ca)"))

def testBrackets(inputString: str) -> bool:
    
    openEnvos: int = 0
    correctlyBracketed: bool = False
    
    for letter in inputString:
        if letter == "(":
            openEnvos += 1
        if letter == ")":
            openEnvos -= 1

    if(abs(openEnvos)==0):
        correctlyBracketed = True
    
    return correctlyBracketed
