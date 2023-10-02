from classes import *
from globalStuff import *
from reg2nea import *
#def tuple2mermaid(automat: Automat) -> MermaidDiagram:
#    mermaid: MermaidDiagram
    
#    return mermaid


def ra2nea(ra: str):
    # Analyze RA
    return


if __name__ == '__main__':
    referenceAutomat = NEA({0, 1, 2}, {"a", "b"}, 0, {(0, "a", 1), (0, "b", 0), (1, "a", 0), (1, "b", 2), (2, "a", 0), (2, "b", 1)}, {2})
    testAutomat1 = NEA({4, 5, 10}, {"a", "b"}, 4, {(4, "a", 5), (4, "b", 4), (5, "a", 4), (5, "b", 10), (10, "a", 4), (10, "b", 5)}, {10})
    
    testAutomat2 = NEA({0, 1, 2, 3}, {"a", "b"}, 0, {(0, "a", 1), (0, "b", 2), (2, "b", 2), (1, eps, 3)}, {3, 0})
    testAutomat3 = NEA({0, 1, 2}, {"a", "b"}, 0, {(0, "a", 0), (0, "b", 1), (1, "b", 2), (2, chr(949), 0)}, {2, 0})
    sampleRegexWithBrackets = ["((a)+(b))", "((((a)+(b))*)(b))", "((((a)+(b))*).((c).(a)))", "((a)*)", "(((a)+(b))*)"]
    #print(testAutomat2.toMermaid())
    #print(testAutomat3.toMermaid())
    #print(unionNEA(testAutomat2, testAutomat3).toMermaid())
    #print(unionNEA(testAutomat2, testAutomat3))
    #print(concatNEA(testAutomat2, testAutomat3).toMermaid())
    #print(kleeneNEA(testAutomat2).toMermaid())
    #print(regexAddBrackets("ab+c*"))
    #print("(Aasdfasdfasdf)"[1:-1])
    # print(regex2nea(sampleRegexWithBrackets[-3]).toMermaid())
    print(f"(1234(What)(())))()), {countBrackets('(1234(What)(())))())')}")

    
    
    
    
    
    