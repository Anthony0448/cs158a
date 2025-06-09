from socket import *

serverPort = 1200

# Make a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind socket to the port
# The empty string means the server will listen on all available interfaces
serverSocket.bind('', serverPort())

# Listen for (one) incoming connections
serverSocket.listen(1)

# Accept
# Accept connection from a client
cnSocket, addr = serverSocket.accept()

# Receive
# Sentance equals the received byte message and is decoded
sentence = cnSocket.recv(64).decode()

# Process
# Convert received message to uppercase
capSentence = sentence.upper()

# Send
# Send back the modified message through the existing socekt (encoded)
cnSocket.send(capSentence.encode())

# Close
# Close connection socket connection with the client
cnSocket.close()
