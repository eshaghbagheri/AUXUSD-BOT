# mt5/position_api.py

class PositionAPI:
    def __init__(self, connector):
        self.mt5 = connector

    def get_all(self):
        return self.mt5.get_positions()

    def close(self, ticket):
        return self.mt5.close_position(ticket)