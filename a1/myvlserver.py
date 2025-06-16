from socket import *

serverPort = 12000

# Make a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind socket to the port
# The empty string means the server will listen on all available interfaces
serverSocket.bind(('', serverPort))

# Listen for (one) incoming connections
serverSocket.listen(1)
print("Listening...")

# Define which first characters represent the length of the message
n = 2

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
    sentence = cnSocket.recv(64).decode()

    msg_len = int(sentence[:n])

    print(f"msg_len: {msg_len}")

    # Process
    # Convert received message to uppercase. Only get the characters after the first n
    processed = sentence[n:].upper()
    print(f"processed: {processed}")

    # Send
    # Send back the modified message through the existing socekt (encoded)
    cnSocket.send(processed.encode())

    msg_len_sent = len(processed)
    print(f"msg_len_sent: {msg_len_sent}")

    # Close
    # Close connection socket connection with the client
    cnSocket.close()
