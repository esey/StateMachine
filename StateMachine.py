import logging
log = logging.getLogger()

import string

class StateMachine:


    def load_transitions(self, filename):

        self.transitions = {}

        plain_table = map(string.split, open(filename).readlines())

        for transition in plain_table:

            if len(transition) > 2:

                state_id, event_id, new_state_id = transition
                if not state_id in self.transitions:
                    self.transitions[state_id] = {}
                self.transitions[state_id][event_id] = new_state_id


    def verify_transitions(self):

        for state_id in self.transitions.keys():
            log.info("Checking state \"%s\"" % state_id)

            for event_id in self.transitions[state_id].keys():
                next_state_id = self.transitions[state_id][event_id]
                if next_state_id != "End":
                    if not next_state_id in self.transitions:
                        log.critical(" - transition: event \"%s\" -> state \"%s\"" % (event_id, next_state_id))
                        log.critical("ERROR: state ", next_state_id, "not defined in transitions table")
                        exit(1)
                    else:
                        log.info(" - transition: event \"%s\" -> state \"%s\"" % (event_id, next_state_id))


    def next_state(self, state_id, event_id):

        log.debug("State: %s" % state_id)
        if not state_id in self.transitions:
            log.critical("Cannot find state %s in transactions table" % state_id)
            exit(1)

        state_transitions = self.transitions[state_id]

        log.debug("Event: %s" % event_id)
        if event_id == None:
            return None

        if event_id in state_transitions:

            next_state = state_transitions[event_id]
            if not next_state in self.state_by_name:
                log.critical("cannot find new state %s" % next_state)
                exit(1)
            return self.state_by_name[next_state]

        else:

            log.critical("ERROR: transition not specified for event: %s" % event_id)
            exit(1)


    def add_state_instance(self, state_instance):
        log.debug("Registering state %s instance" % state_instance.id)
        self.state_by_name[state_instance.id] = state_instance


    def verify_state_instances(self):

        log.info("Verifying states instantiation.")

        for state_id in self.transitions.keys():
            log.info("Checking source state \"%s\"" % state_id)

            if state_id not in self.state_by_name:
                log.critical("Source state %s not instantiated" % state_id)
                exit(1)

            for event_id in self.transitions[state_id].keys():
                next_state_id = self.transitions[state_id][event_id]
                log.info("Checking destination state \"%s\"" % next_state_id)
                if next_state_id not in self.state_by_name:
                    log.critical("Destination state %s not instantiated" % nest_state_id)
                    exit(1)

    def run_all(self):

        if not "Start" in self.state_by_name:
            log.info("ERROR: \"Start\" state not defined")
            exit(1)

        state = self.state_by_name["Start"]

        while state != None:

            event = state.run()

            if event != None:
                log.debug("State %s returned event: %s" % (state.id, event.id))
                old_state = state
                state = self.next_state(state.id, event.id)
                log.debug("%s -> %s -> %s" % (old_state.id, event.id, state.id))
            else:
                log.info("State %s returned \"None\" event. Terminating the state machine..." % state.id)
                return None



    def __init__(self, trans_table_file):

        log.info("State machine initialization")

        self.transitions = {}
        self.state_by_name = {}

        self.load_transitions(trans_table_file)

        log.info("Verifying transitions coherence...")
        self.verify_transitions()
        log.info("Transitions are coherent.")