# api/routes.py

from fastapi import FastAPI, WebSocket
from core.config_manager import ConfigManager
from core.state_manager import StateManager

app = FastAPI()

config = ConfigManager()
state = StateManager()

bot_instance = None  # در main.py inject می‌شود


# -------------------------
# Inject bot
# -------------------------

def set_bot_instance(bot):
    global bot_instance
    bot_instance = bot


# -------------------------
# Control APIs
# -------------------------

@app.post("/start")
def start_bot():
    if bot_instance:
        bot_instance.start()
    return {"status": "started"}


@app.post("/stop")
def stop_bot():
    if bot_instance:
        bot_instance.stop()
    return {"status": "stopped"}


@app.post("/close-profit")
def close_profit():
    if bot_instance:
        bot_instance.order_manager.close_profitable()
    return {"status": "profit_closed"}


@app.post("/close-loss")
def close_loss():
    if bot_instance:
        bot_instance.order_manager.close_losing()
    return {"status": "loss_closed"}


# -------------------------
# Config APIs
# -------------------------

@app.get("/config")
def get_config():
    return config.get_all()


@app.post("/config")
def update_config(data: dict):
    config.update(data, auto_save=True)
    return {"status": "updated"}


# -------------------------
# Status
# -------------------------

@app.get("/status")
def status():
    return {
        "state": state.get_state(),
        "running": state.is_running()
    }


# -------------------------
# WebSocket
# -------------------------

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        if bot_instance:
            data = {
                "state": state.get_state(),
                "profit": bot_instance.position_tracker.get_profit(),
                "positions": bot_instance.position_tracker.count()
            }

            await websocket.send_json(data)