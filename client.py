import socket
import threading
import sys


if len(sys.argv) != 3:
    print("Error: IP address, port")
    exit()


host = sys.argv[1]
port = int(sys.argv[2])


# Asks for nickname
nickname = input('Choose your nickname: ')


# Connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# Listens to server 
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('An error occured!')
            client.close()
            break


# Sends messages to server
def write():
    while True:
        message = '{}: {}'.format(nickname, input('> '))
        client.send(message.encode('utf-8'))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()