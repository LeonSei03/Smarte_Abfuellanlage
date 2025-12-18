import logging
from nfc_reader import NFCReader

# Configure the logger
logger = logging.getLogger("shared_logger")
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)



class StateMachine:
    def __init__(self):
        self.current_state = 'State0'
        self.reader = None
        self.states = {
            'State0': State0(self),
            'State1': State1(self),
            'State2': State2(self),
            'State3': State3(self),
            'State4': State4(self),
            'State5': State5(self)
        }

    def run(self):
        # Run the state machine until it reaches a terminal state
        # To run indefinitely, remove the terminal states from the while loop
        while self.current_state not in ['State4','State5']:
            state = self.states[self.current_state]
            state.run()  # Run the current state

class State:
    def __init__(self, machine):
        self.machine = machine

    def run(self):
        raise NotImplementedError("State must implement 'run' method.")

class State0(State):
    def run(self):
        logging.info("Initializing RFID reader...")
        
        # Simulate RFID reader initialization (replace with actual initialization code)
        self.machine.reader = NFCReader()
        if self.machine.reader:
            init_successful = True  # Simulate success
        
        if init_successful:
            logging.info("RFID reader initialized successfully.")
            self.machine.current_state = 'State1'  # Transition to State1
        else:
            logging.error("Failed to initialize RFID reader.")
            self.machine.current_state = 'State5'  # Transition to State5

class State1(State):
    def run(self):
        logging.info("Waiting for RFID card...")
        
        # Simulate card detection (replace with actual detection code)
        uid = [45, 162, 193, 56]  # Placeholder for RFID detection
        uid = self.machine.reader.read_passive_target(timeout=0.5)
        if uid is None:
            logging.warning("No card detected. Retrying...")
            self.machine.current_state = 'State1'  # Wait again
        else:
            logging.info(f"Found card with UID: {[hex(i) for i in uid]}") 
            self.machine.current_state = 'State2'  # Transition to State2

class State2(State):
    def run(self):
        logging.info("Writing Bottle ID to card...")
        
        # Simulate writing logic
        write_successful = True  # Simulate success
        
        if write_successful:
            logging.info("Successfully wrote to card.")
            self.machine.current_state = 'State3'  # Transition to State3
        else:
            logging.error("Failed to write to card. Waiting for a new card.")
            self.machine.current_state = 'State1'  # Transition back to State1

class State3(State):
    def run(self):
        logging.info("Saving Bottle ID and timestamp to database...")
        
        # Simulate database write (replace with actual database code)
        db_write_successful = True  # Simulate success
        
        if db_write_successful:
            logging.info("Successfully saved to database.")
            self.machine.current_state = 'State4'  # Transition to State4
        else:
            logging.error("Failed to save data to database.")
            self.machine.current_state = 'State5'  # Transition to State5

class State4(State):
    def run(self):
        logging.info("Successfully completed the process! Returning to State1.")
        
        # Transition back to State1 - probably not hepful while debugging
        #self.machine.current_state = 'State1'  

class State5(State):
    def run(self):
        logging.error("Process failed at some point. Please check the logs.")
        self.machine.current_state = 'State5'  # End of process

# Main execution
if __name__ == '__main__':
    machine = StateMachine()
    machine.run()
    logging.info("Stopped Execution. Please rerun the program to start again.")