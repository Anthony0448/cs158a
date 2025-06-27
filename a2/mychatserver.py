from socket import *
from threads import *

serverPort = 12000

# TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind socket to the port
serverSocket.bind(('', serverPort))

# Listen for incoming connections
serverSocket.listen(1)
print("Listening...")

# Server keeps running even after one message is received
while True:
    # Accept
    # Accept connection from a client
    cnSocket, addr = serverSocket.accept()
    # Print address of connected client
    # Also prints port which is a random port the client's machine finds that is open.
    print(f"Connection from {addr}")

    # Receive
    # Sentance equals the received byte message and is decoded
    message = cnSocket.recv(1024).decode()

    # Process
    # Convert received message to uppercase
    capMessage = message.upper()

    # Send
    # Send back the modified message through the existing socekt (encoded)
    # cnSocket.send(capSentence.encode())

    # Just print message for now to ensure it was received
    print(f"{addr}: {capMessage}")

    # Close
    # Close connection socket connection with the client
    if message.strip().lower() == 'exit':
        cnSocket.close()
