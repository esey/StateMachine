import logging
log = logging.getLogger()

class State:

    id = "state-id-not-initialized"

    def run(self):
        assert 0, "run not implemented"

    def produce_event(self, event):
        log.info("New event: %s " % event.id)