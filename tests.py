import pytest
from globalStuff import *
from classes import *

# def testRenameNodes():
#     referenceAutomat = NEA({0, 1, 2}, {"a", "b"}, 0, {(0, "a", 1), (0, "b", 0), (1, "a", 0), (1, "b", 2), (2, "a", 0), (2, "b", 1)}, {2})
#     testAutomat1 = NEA({4, 5, 10}, {"a", "b"}, 4, {(4, "a", 5), (4, "b", 4), (5, "a", 4), (5, "b", 10), (10, "a", 4), (10, "b", 5)}, {10})
#    assert renameStates(testAutomat1, 0).relation == referenceAutomat.relation

class TestReg2Nea(unit)