import asyncio
import random
import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import configparser
import sys
import json
import websockets

log_folder = '/var/log/chat_room'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, 'server.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=7)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logging.getLogger('').addHandler(log_handler)

# Variable globale pour stocker les clients connectés
CLIENTS = {}

async def handle_client(websocket, path):
    client_address = websocket.remote_address
    logging.info(f"Client connected from {client_address[0]}:{client_address[1]}")

    # Vérifier si le client est déjà dans la liste des clients
    if client_address not in CLIENTS:
        # Attendre le message initial du client
        data = await websocket.recv()
        if not data:
            return
        
        message = json.loads(data)
        id = message.get('id', None)

        if id == 1:
            pseudo = message.get('pseudo', '')

            # Ajouter le nouveau client à la liste des clients avec le pseudo
            CLIENTS[client_address] = {"ws": websocket, "pseudo": pseudo, "color": random.randint(0, 255)}

            hours = datetime.datetime.now().hour
            minutes = datetime.datetime.now().minute

            # Envoyer une annonce à tous les clients
            announcement = f"{pseudo} a rejoint la chatroom"
            encoded_announcement = {
                "id": 1,
                "hours": hours,
                "minutes": minutes,
                "length": len(announcement),
                "announcement": announcement
            }
            await broadcast_message(encoded_announcement, client_address)

            logging.info(f"Added client {client_address[0]}:{client_address[1]} to CLIENTS with pseudo {pseudo}")

    try:
        while True:
            data = await websocket.recv()
            if not data:
                break

            print(data)

            message = json.loads(data)
            print(message)
            id = message.get('id', None)

            if id == 0:
                length = message.get('length', 0)
                message_text = message.get('message', '')

                logging.info(f"Received message from client {client_address[0]}:{client_address[1]}: {message_text}")

                # Vérifier si le message est un message de déconnexion
                if message_text.strip() == "":
                    break

                self_encoded_message = {
                    "id": 2,
                    "hours": datetime.datetime.now().hour,
                    "minutes": datetime.datetime.now().minute,
                    "color": CLIENTS[client_address]["color"],
                    "length": len(message_text),
                    "message": message_text
                }
                await CLIENTS[client_address]["ws"].send(json.dumps(self_encoded_message))

                hours = datetime.datetime.now().hour
                minutes = datetime.datetime.now().minute

                # Envoyer le message à tous les clients
                for addr, client_info in CLIENTS.items():
                    if addr != client_address:
                        # Construire le message avec le pseudo du client
                        encoded_message = {
                            "id": 0,
                            "hours": hours,
                            "minutes": minutes,
                            "color": CLIENTS[client_address]["color"],
                            "pseudo_length": len(CLIENTS[client_address]["pseudo"]),
                            "pseudo": CLIENTS[client_address]["pseudo"],
                            "length": len(message_text),
                            "message": message_text
                        }
                        await client_info["ws"].send(json.dumps(encoded_message))

    except asyncio.CancelledError:
        pass

    logging.info(f"Client {client_address[0]}:{client_address[1]} disconnected")

    hours = datetime.datetime.now().hour
    minutes = datetime.datetime.now().minute

    # Envoyer un message d'annonce à tous les clients
    announcement = f"{CLIENTS[client_address]['pseudo']} a quitté la chatroom"
    encoded_announcement = {
        "id": 1,
        "hours": hours,
        "minutes": minutes,
        "length": len(announcement),
        "announcement": announcement
    }
    await broadcast_message(encoded_announcement, client_address)
    
    del CLIENTS[client_address]

async def broadcast_message(message, exclude_address):
    for addr, client_info in CLIENTS.items():
        if addr != exclude_address:
            await client_info["ws"].send(json.dumps(message))

def read_config():
    if not os.path.exists('config.ini'):
        raise FileNotFoundError("ERROR Le fichier de configuration n'existe pas. Veuillez créer un fichier config.ini avec les paramètres suivants:\n[DEFAULT]\nhost = <ip_address>\nport = <port_number>")
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']['host'], int(config['DEFAULT']['port'])

def parse_command_line():
    if len(sys.argv) in [3, 5]:
        host, port = read_config()
        for i in range(1, len(sys.argv), 2):
            if sys.argv[i] in ['-p', '--port'] and 0 <= int(sys.argv[i + 1]) <= 65535:
                port = int(sys.argv[i + 1])
                if 0 <= port <= 1024:
                    raise ValueError("ERROR Le port spécifié est un port privilégié. Spécifiez un port au-dessus de 1024.")
            elif sys.argv[i] in ['-a', '--address']:
                host = sys.argv[i + 1]
            elif sys.argv[i] in ['-h', '--help']:
                print("Usage: python3 client.py [-a <ip_address>] [-p <port_number>]")
                sys.exit(2)
        return host, port

async def start_server():

    host, port = parse_command_line() if len(sys.argv) in [3, 5] else read_config()

    server = await websockets.serve(
        handle_client, host, port)

    addr = server.sockets[0].getsockname()
    print(f"Server listening on {addr[0]}:{addr[1]}")
    logging.info(f"Server listening on {addr[0]}:{addr[1]}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_server())
