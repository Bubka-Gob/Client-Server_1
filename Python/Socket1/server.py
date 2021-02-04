import socket
import threading
import time
import datetime

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
RECONNECT_MESSAGE = '!RECONNECT'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #get local ip
ADDR = (SERVER, PORT)
NAME_MARK = '!NAME '

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
active_connections = {}

def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' *(HEADER - len(msg_length)) #adding byte-spaces to get length of HEADER
    conn.send(msg_length)
    conn.send(message)
def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)  # HEADER - length of thirst message, which contains length of main message
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg
    return None
def update_chat(msg, name):
    print(name)
    for key in active_connections.keys():
        send(name, key)
        send(msg, key)
        send(f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}', key)

def handle_client(conn, addr):
    time.sleep(0.001)
    print('Connected:', addr)
    connected =True
    while connected:
        msg = receive(conn)
        if msg != None:
            if NAME_MARK in msg:
                name = msg.split(' ')[1]
                active_connections[conn] = name
                print(active_connections.values())
                update_chat('[CONNECTED]', name)
            elif RECONNECT_MESSAGE in msg:
                name = msg.split(' ')[1]
                update_chat(f'{active_connections[conn]} become a {name}', name)
                active_connections[conn] = name
                print(active_connections.values())
            elif msg == DISCONNECT_MESSAGE:
                update_chat('[DISCONNECTED]', active_connections[conn])
                del active_connections[conn]
                connected = False
            else:
                update_chat(msg, active_connections[conn])
            print(addr, ': ', msg)
    print('Disconnected:', addr)

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print('Active connections:', len(active_connections))

print('Starting Server on IP:', SERVER)
start()