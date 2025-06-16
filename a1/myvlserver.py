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
    cnSocket, client_address = serverSocket.accept()

    # Print address of connected client
    # Also prints port which is a random port the client's machine finds that is open.
    print(f"Connection from {client_address[0]}")

    # The b is needed to make it a byte string since the data is in bytes
    received_data = b''

    # Receive the message in chunks of 64 bytes until the entire message is received
    while True:
        chunk = cnSocket.recv(64)

        # If no more data is received end loop
        if not chunk:
            break

        # Add the chunks together into received_data to form the entire message
        received_data += chunk

        # Make sure that the message has at least the byte length specified (2 bytes)
        if len(received_data) >= n:
            # Get the length of the message
            msg_len = int(received_data[:n].decode())

            # If the message has at least the byte length specified by the prefix, break otherwise keep looping (receiving)
            if len(received_data) >= msg_len + n:
                break

    # Decode the message
    sentence = received_data.decode()

    # Get the length of the message again
    # We use :n because the first n bytes are the length prefix
    msg_len = int(sentence[:n])
    print(f"msg_len: {msg_len}")

    # Process
    # Convert received message to uppercase. Only get the characters after the first n
    processed = sentence[n:].upper()
    print(f"processed: {processed}")

    # Prepare response with length prefix
    response_len = str(len(processed))

    # Add the length prefix to the message
    # This is needed because the client needs to know the length of the message
    # to receive it in order to know when to stop receiving
    full_response = response_len + processed

    # Send response in chunks of 64
    encoded_response = full_response.encode()
    for i in range(0, len(encoded_response), 64):
        chunk = encoded_response[i:i+64]

        cnSocket.send(chunk)

    # Print the length of the message that was sent
    msg_len_sent = len(processed)
    print(f"msg_len_sent: {msg_len_sent}")

    # Close connection socket connection with the client
    cnSocket.close()
    print("Connection closed")
