from socket import *

serverPort = 1200

# Make a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind socket to the port
# The empty string means the server will listen on all available interfaces
serverSocket.bind(('', serverPort))

# Listen for (one) incoming connections
serverSocket.listen(1)
print("Listening...")

# Server keeps running even after one message is received
while True:
    # Accept
    # Accept connection from a client
    cnSocket, addr = serverSocket.accept()
    # Print address of connected client
    print(f"Connection from {addr}")

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