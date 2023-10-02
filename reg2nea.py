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


def regex2nea(regex: str) -> Automat:
    autoOut: NEA
    # Annahme: Der String ist perfekt geklammert, niemals befinden sich zwei Operanden direkt in derselben Klammer
    operationName = str()
    operation: dict ={
        "concat": concatNEA,
        "union": unionNEA
    }
    
    regex = regex[1:-1]
    # Atomare Automaten
    if(len(regex)==1):
        autoOut = SingleCharNEA(regex)
        return autoOut
    
    # Kleene bestimmen
    if(regex[-1]=='*'):
        return kleeneNEA(regex2nea(regex[:-1]))
    
    # Position union/concat
     
    posOperation: int = countBrackets(regex).index(0)+1
    
    # Operation bestimmen
    if regex[posOperation:posOperation+1]=='+':
        operationName = "union"
    else:
        operationName = "concat"
    
    # Operanden bestimmen

    operandOne: str = regex[:posOperation]
    operandTwo: str = regex[posOperation+1:]
    
    autoOne = regex2nea(operandOne)
    autoTwo = regex2nea(operandTwo)
    
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

def regexAddBrackets(regex: str) -> str:

    # encapsulate letters
    alphabet: set = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
    for letter in alphabet:
        regex = regex.replace(letter, f"({letter})")
    
    # encapsulate kleenes
    # pseudo code:
    #   nächsten Kleene finden
    #   positionen (links und rechts) finden
    #   neuen String zusammenbasteln

    posStar = regex.rfind("*")
    while not posStar==-1:
        
        bracketList: list = countBrackets(regex[:posStar])
        depthStar = bracketList[posStar-1]
        
        # find positions
        rIndex = posStar+1
        lIndex = rindex(bracketList[:posStar-1], depthStar)
        
        # build new String
        regex = f"{regex[:lIndex+1]}({regex[lIndex+1:rIndex]}){regex[rIndex:]}"
        posStar = regex[:posStar].rfind("*")

    # add concat
    regex = regex.replace(")(", f").(")
    
    # encapsulate union
    
    return regex

def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1