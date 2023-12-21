# from https://websockets.readthedocs.io/en/stable/howto/quickstart.html
import asyncio
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")
    await websocket.send(f"Hello client ! Received {name}")


async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
