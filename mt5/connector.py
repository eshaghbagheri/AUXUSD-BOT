# mt5/connector.py

import MetaTrader5 as mt5


class MT5Connector:
    def __init__(self, config):
        self.config = config

        self.symbol = config.get_str("symbol", "XAUUSDm")
        self.connected = False

        # optional account config (if provided)
        self.account = config.get("account")
        self.password = config.get("password")
        self.server = config.get("server")

    # -------------------------
    # Connection
    # -------------------------

    def connect(self):
        """Initialize MT5 and login if credentials exist"""
        try:
            if not mt5.initialize():
                print("❌ MT5 initialize failed")
                return False

            # login if credentials exist
            if self.account and self.password and self.server:
                login_result = mt5.login(
                    self.account,
                    password=self.password,
                    server=self.server
                )

                if not login_result:
                    print("❌ MT5 login failed")
                    mt5.shutdown()
                    return False

            self.connected = True
            print("✅ MT5 connected successfully")
            return True

        except Exception as e:
            print(f"❌ MT5 connection error: {e}")
            return False

    def shutdown(self):
        """Shutdown MT5 connection"""
        try:
            mt5.shutdown()
        finally:
            self.connected = False

    # -------------------------
    # Status
    # -------------------------

    def is_connected(self):
        return self.connected and mt5.terminal_info() is not None

    # -------------------------
    # Market data
    # -------------------------

    def get_symbol(self):
        return self.symbol

    def get_tick(self, symbol=None):
        """Get latest tick data"""
        sym = symbol or self.symbol

        tick = mt5.symbol_info_tick(sym)
        if tick is None:
            return None

        return {
            "bid": tick.bid,
            "ask": tick.ask,
            "last": tick.last,
            "time_msc": tick.time_msc,
            "volume": tick.volume
        }

    def get_symbol_info(self, symbol=None):
        sym = symbol or self.symbol
        return mt5.symbol_info(sym)

    # -------------------------
    # Trading
    # -------------------------

    def send_order(self, request: dict):
        """
        Send raw order request to MT5
        request example:
        {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": "XAUUSDm",
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_BUY,
            "price": 0.0,
            "deviation": 20,
            "magic": 123456,
            "comment": "bot order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        """
        try:
            result = mt5.order_send(request)

            if result is None:
                print("❌ order_send returned None")
                return None

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"⚠️ Order failed: {result.retcode}")

            return result

        except Exception as e:
            print(f"❌ send_order error: {e}")
            return None

    # -------------------------
    # Positions
    # -------------------------

    def get_positions(self, symbol=None):
        sym = symbol or self.symbol

        positions = mt5.positions_get(symbol=sym)
        if positions is None:
            return []

        return list(positions)

    def close_position(self, ticket):
        """Close a specific position by ticket"""
        try:
            position = mt5.positions_get(ticket=ticket)
            if not position:
                return False

            pos = position[0]

            # opposite order for closing
            order_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": order_type,
                "position": ticket,
                "price": mt5.symbol_info_tick(pos.symbol).bid,
                "deviation": 20,
                "magic": pos.magic,
                "comment": "close position",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            return result

        except Exception as e:
            print(f"❌ close_position error: {e}")
            return False