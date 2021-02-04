import socket
import sys
import gui
import threading

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
RECONNECT_MESSAGE = '!RECONNECT '
NAME_MARK = '!NAME '
PORT = 5050
FIELD_NAME = []
FIELD_CHAT = []
FIELD_MESSAGE = []
SERVER = '192.168.2.2'
ADDR = (SERVER, PORT)
is_connected = [False]
#chat_messages = []

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' *(HEADER - len(msg_length)) #adding byte-spaces to get length of HEADER
    client.send(msg_length)
    client.send(message)
def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)  # HEADER - length of thirst message, which contains length of main message
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return msg
def update():
    new_message = []
    while is_connected:
        new_message.append(receive()) #get name
        new_message.append(receive()) #get message
        new_message.append(receive()) #get date
        #chat_messages.append(new_message)
        FIELD_CHAT[0].append(f'{new_message[0]}: {new_message[1]} ({new_message[2]})')
        new_message = []

def send_pressed():
    if len(FIELD_MESSAGE[0].toPlainText()) != 0:
        send(FIELD_MESSAGE[0].toPlainText())
def connect_pressed():
    if len(FIELD_NAME[0].text()) == 0 or len(FIELD_NAME[0].text()) >16 or ' ' in FIELD_NAME[0].text():
        FIELD_NAME[0].setText('Incorrect name')
    elif is_connected[0]:
        send(RECONNECT_MESSAGE + FIELD_NAME[0].text()) #change name
    else:
        client.connect(ADDR)
        send(NAME_MARK + FIELD_NAME[0].text())
        is_connected[0] = True
        updating_thread = threading.Thread(target=update)
        updating_thread.start()

def get_fields(field_name, field_chat, field_message):
    FIELD_NAME.append(field_name)
    FIELD_CHAT.append(field_chat)
    FIELD_MESSAGE.append(field_message)

def start_gui():
    app = gui.QtWidgets.QApplication(sys.argv)
    MainWindow = gui.QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow, connect_pressed, send_pressed, get_fields)
    MainWindow.show()
    sys.exit(app.exec_())

gui_Thread = threading.Thread(target=start_gui)
gui_Thread.start()
gui_Thread.join() # waiting for gui to close
send(DISCONNECT_MESSAGE)
