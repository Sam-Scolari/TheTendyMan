import os
import server
import asyncio

def start_server():
    os.system('start ngrok http 5000')
    server.app.run()


if __name__ == "__main__":
    start_server()