from socket import *

# serverName = '192.168.1.2'  # ip address
serverName = 'localhost'
serverPort = 12000  # port number

# TCP SOCKET_STREAM
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to server
clientSocket.connect((serverName, serverPort))

sentence = input('Enter a lowercase sentence: ')

# .encode returns the string encoded to bytes. The server decodes this when it is read
clientSocket.send(sentence.encode())  # Send sentence to server

modifiedSentence = clientSocket.recv(64)

print('From Server:', modifiedSentence.decode())

clientSocket.close()
