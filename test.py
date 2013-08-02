import string, os, sys, time
sys.path.insert(0, os.path.join(os.getcwd(), "StateMachine"))

from StateMachine import StateMachine
from State import State
from Event import Event

dummyEvent = Event("dummy_event")
eventStart = Event("eventStart")
event0 = Event("event0")
event1 = Event("event1")
event2 = Event("event2")
eventEnd = Event("eventEnd")

class dummyState(State):

    id = "dummy_state"

    def run(self):
        return dummyEvent


class Start(State):

    id = "Start"

    def run(self):
        return eventStart


class A(State):

    id = "A"

    def run(self):
        return event0


class B(State):

    id = "B"

    def run(self):
        return event1


class C(State):

    id = "C"

    def run(self):
        return event2


class D(State):

    id = "D"

    def run(self):
        return None

# End of test classes
#------------------------------------------------------------------------------

def test_emptyState():
    state = State()

    assert state.id == "state-id-not-initialized"


def test_dummyState():

    state = dummyState();

    assert state
    assert state.id == "dummy_state"


def test_dummyStateRun():

    state = dummyState();

    assert state
    assert state.id == "dummy_state"

    event = state.run()

    assert event.id == "dummy_event"


def test_emptyEvent():
    event = Event("dummy_event")

    assert event.id == "dummy_event"


def test_events():

    assert eventStart.id == "eventStart"
    assert event0.id == "event0"
    assert event1.id == "event1"
    assert event2.id == "event2"


def test_StateClasses():

    assert Start.id == "Start"
    assert A.id == "A"
    assert B.id == "B"
    assert C.id == "C"
    assert D.id == "D"


def test_StateInstances():

    stateStart = Start()
    stateA = A()
    stateB = B()
    stateC = C()
    stateD = D()

    assert stateStart.id == "Start"
    assert stateA.id == "A"
    assert stateB.id == "B"
    assert stateC.id == "C"
    assert stateD.id == "D"

    assert stateStart.run() == eventStart
    assert stateA.run() == event0
    assert stateB.run() == event1
    assert stateC.run() == event2
    assert stateD.run() == None

def test_StateMachineInstantiation():

    SM = StateMachine("test_table.txt")
    assert True

def test_stateMachineTransTableNotExists():
    try:
        SM = StateMachine("not-existing-file.txt")
    except IOError:
        assert True

#def test_stateMachineWrongTable0():
    #try:
        #SM = StateMachine("wrong_table0.txt")
    #except IOError:
        #assert True

#def test_stateMachineWrongTable1():
    #try:
        #SM = StateMachine("wrong_table1.txt")
    #except IOError:
        #assert True

def test_stateMachineWrongTable2():
    try:
        SM = StateMachine("wrong_table2.txt")
    except IOError:
        assert True


def test_stateMachineRun():

    SM = StateMachine("test_table.txt")

    stateStart = Start()
    stateA = A()
    stateB = B()
    stateC = C()
    stateD = D()

    SM.addStateInstance(stateStart)
    SM.addStateInstance(stateA)
    SM.addStateInstance(stateB)
    SM.addStateInstance(stateC)
    SM.addStateInstance(stateD)

    assert SM.runAll() == None
