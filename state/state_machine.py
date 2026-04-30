# state/state_machine.py


class StateMachine:
    def __init__(self, state_manager, event_bus):
        self.state = state_manager
        self.bus = event_bus

        self.transitions = {
            "IDLE": ["SCANNING"],
            "SCANNING": ["SIGNAL", "IDLE"],
            "SIGNAL": ["BURST", "SCANNING"],
            "BURST": ["MANAGING", "COOLDOWN"],
            "MANAGING": ["EXIT", "COOLDOWN"],
            "EXIT": ["COOLDOWN"],
            "COOLDOWN": ["IDLE"]
        }

    # -------------------------
    # Validate transition
    # -------------------------

    def can_transition(self, new_state: str):
        current = self.state.get_state()
        return new_state in self.transitions.get(current, [])

    # -------------------------
    # Apply transition
    # -------------------------

    def transition(self, new_state: str):
        if not self.can_transition(new_state):
            return False

        prev = self.state.get_state()
        self.state.set_state(new_state)

        self.bus.publish("state_changed", {
            "from": prev,
            "to": new_state
        })

        return True