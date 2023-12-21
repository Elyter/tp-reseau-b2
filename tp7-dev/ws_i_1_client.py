# from https://websockets.readthedocs.io/en/stable/howto/quickstart.html
import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    while True:
        async with websockets.connect(uri) as websocket:
            message = input("message: ")

            await websocket.send(message)
            print(f">>> {message}")

            greeting = await websocket.recv()
            print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())
