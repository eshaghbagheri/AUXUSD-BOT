# mt5/order_api.py

class OrderAPI:
    def __init__(self, connector):
        self.mt5 = connector

    def send(self, request):
        return self.mt5.send_order(request)

    def close(self, ticket):
        return self.mt5.close_position(ticket)