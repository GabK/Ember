import json
from pyrevogi import Bulb
from tornado import websocket, web, ioloop

bulb = Bulb("D0:5F:B8:27:BD:A8")

class LightbulbWebSocketHandler(websocket.WebSocketHandler):
    def on_message(self, message):
        msg = json.loads(message)

        if "status" in msg:
            if msg["status"]:
                bulb.on()
            elif not msg["status"]:
                bulb.off()
        elif "brightness" in msg:
            bulb.set(brightness = msg["brightness"])

class DashboardHandler(web.RequestHandler):
    def get(self):
        self.render("templates/dashboard.html", is_on=bulb.is_on(), brightness=bulb.brightness)

def make_app():
    return web.Application([
        (r"/", DashboardHandler),
        (r'/lightbulb', LightbulbWebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    ioloop.IOLoop.current().start()