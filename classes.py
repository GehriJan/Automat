from globalStuff import *

class Automat:
    states: set = set()
    alphabet: set = set()
    startState: int
    relation = set()
    endStates: set = set()

    def __init__(
        self,
        states=None,
        alphabet=None,
        startState=0,
        relation=None,
        endStates=None,
    ):
        self.startState = startState

        if states:
            self.states = states
        if alphabet:
            self.alphabet = alphabet
        if relation:
            self.relation = relation
        if endStates:
            self.endStates = endStates
        self.states.add(startState)

    def __str__(self) -> str:
        return f"States: {self.states}\nAlphabet: {self.alphabet}\nStartState: {self.startState}\nRelation: {self.relation}\nEndstates: {self.endStates}\n"

    def __eq__(self, otherAutomat) -> bool:
        return (
            self.states == otherAutomat.states
            and self.alphabet == otherAutomat.alphabet
            and self.startState == otherAutomat.startState
            and self.relation == otherAutomat.relation
            and self.endStates == otherAutomat.endStates
        )
    def toMermaid(self) -> str:
        output: str =   "flowchart LR\
                        \n\tclassDef default stroke:black,fill:white;"
        for state in self.states:
            if({state}.issubset(self.endStates)):
                output += f"\n\t{state}((({state})))"
            else:
                output += f"\n\t{state}(({state}))"
        for change in self.relation:
            output += f"\n\t{change[0]}-- {change[1]} -->{change[2]}"
        return output

class NEA(Automat):
    def __init__(
        self, states=None, alphabet=None, startState=0, relation=None, endStates=None
    ):
        super().__init__(states, alphabet, startState, relation, endStates)
        self.alphabet.add(eps)


class EmptyLangNEA(NEA):
    def __init__(self):
        super().__init__(self)


class EmptyWordNEA(NEA):
    def __init__(self):
        super().__init__(self)
        self.endStates.add(0)


class SingleCharNEA(NEA):
    def __init__(self):
        super().__init__(self)
        self.states.add(1)
        self.alphabet.add(
            "v"
        )  # todo: wie mache ich das, dass die Mengeneinträge geändert werden, wenn atomare Automaten hinzugefügt werden?
        self.relation.add((0, "v", 1))
        self.endStates.add(1)
    

def renameStates(auto: Automat, index: int) -> Automat:
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
                
            auto.relation.discard(change)
            auto.relation.add(tuple(tempList))
        # Neue Endzustände
        for endState in auto.endStates:
            if state == endState:
                auto.endStates.discard(state)
                auto.endStates.add(index)
                break
        # Ändere Vorkommen in Zuständen
        auto.states.discard(state)
        auto.states.add(index)

        index = index + 1

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