import socket
import threading
from p4c_Client import *


class Client(threading.Thread):

    def __init__(self, id):
        threading.Thread.__init__(self)

        self.id1 = id
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(("localhost", 1111))

    def send(self, data):
        self.clientsocket.send((data.encode()))

    def receive(self):
        data = self.clientsocket.recv(2048).decode()
        if data == "exit":
            self.clientsocket.send(data.encode())
            self.isRunning = False
        else:
            return data

    def run(self):
        print("Client lancée...")
        self.send(self.id1)
        self.id2 = self.receive()
        print("Vous jouez avec :", self.id2)

        p4c(self, self.id2, self.id1, False)

        self.clientsocket.close()
