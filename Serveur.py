import threading
from p4c_Server import *

class Serveur(threading.Thread):

    def __init__(self, ip, port, clientsocket, id):
        threading.Thread.__init__(self)

        self.id1 = id
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket

        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def send(self, data):
        self.clientsocket.send(data.encode())

    def receive(self):
        data = self.clientsocket.recv(2048).decode()
        if data == "exit":
            self.clientsocket.send(data.encode())
            self.isRunning = False
        else:
            return data

    def run(self):
        self.id2 = self.receive()
        print("Serveur lancée...")
        print("Vous jouez avec :", self.id2)
        self.send(self.id1)

        p4c(self, self.id1, self.id2, True)






