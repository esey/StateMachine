import string

class StateMachine:


    def loadTransitions(self, filename):

        self.transitions = {}

        plain_table = map(string.split, open(filename).readlines())

        for transition in plain_table:

            if len(transition) > 2:

                state_id, event_id, new_state_id = transition
                if not state_id in self.transitions:
                    self.transitions[state_id] = {}
                self.transitions[state_id][event_id] = new_state_id

        print self.transitions


    def verifyTransitions(self):

        print self.transitions

        for state_id in self.transitions.keys():
            print "Checking... ", state_id

            for event_id in self.transitions[state_id].keys():
                next_state_id = self.transitions[state_id][event_id]
                if next_state_id != "End":
                    if not next_state_id in self.transitions:
                        print "ERROR: state ", next_state_id, "not defined in transitions table"
                        exit(1)


    def nextState(self, state_id, event_id):

        if not state_id in self.transitions:
            print "cannot find transaction table"
            exit(1)

        state_transitions = self.transitions[state_id]

        if event_id == None:
            return None

        if event_id in state_transitions:

            next_state = state_transitions[event_id]
            if not next_state in self.stateByName:
                print "cannot find new state"
                exit(1)
            return self.stateByName[next_state]

        else:

            print "ERROR: transition not specified for event: ", event_id
            exit(1)


    def addStateInstance(self, state_instance):
        self.stateByName[state_instance.id] = state_instance


    def runAll(self):

        if not "Start" in self.stateByName:
            print "ERROR: \"Start\" state not defined"
            exit(1)

        state = self.stateByName["Start"]
        while state != None:
            event = state.run()
            if event != None:
                state = self.nextState(state.id, event.id)
            else:
                return None


    def __init__(self, trans_table_file):

        print "State machine initialization"

        self.transitions = {}
        self.stateByName = {}

        self.loadTransitions(trans_table_file)

        print "Verifying state machine..."
        self.verifyTransitions()
        print "Verification done."