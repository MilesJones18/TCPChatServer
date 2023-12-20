import socket
import threading
import sys

# Check the arguments.
if len(sys.argv) != 3:
    print("Error: IP address, port")
    exit()


# Take each arguement as IP and port respectively
host = sys.argv[1]

port = int(sys.argv[2])


# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


# List client/nicknames
clients = []
nicknames = []


# Send messages
def broadcast(message):
    for client in clients:
        client.send(message)


# Handle messages
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break


# Receive messages
def recieve():
    while True:
        # Accepts connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Asks for and stores the nickname of the connecting user
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Prints and broadcasts the new nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("|-----Server up-----|")
recieve()