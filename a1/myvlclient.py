from socket import *

server_name = 'localhost'
server_port = 12000

# TCP SOCK_STREAM
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to server and pass the address information (port & server name)
clientSocket.connect((server_name, server_port))

# First n bytes is the length of the message
n = 2

# Loop while first n characters are not digits
while True:
    original_sentence = input(
        f"Input lowercase sentence (first {n} characters are message length): ")

    # Make sure the input is at least n characters long and those first n characters are digits
    if len(original_sentence) >= n and original_sentence[:n].isdigit() and len(original_sentence) == int(original_sentence[:n]) + n:
        break
    else:
        print(
            f"Invalid input. The first {n} characters must be digits and the size must match. Please try again.")

encoded_original_sentence = original_sentence.encode()

# Send message in chunks of 64 (buffsize 64)
# Increment up to encoded sentence length by 64 each loop
for i in range(0, len(encoded_original_sentence), 64):
    # Extract bytes from i to (i + 64) ; Like take bytes from 0 to 0 + 64 then 64 to 128
    chunk = encoded_original_sentence[i:i+64]

    # Send each 64 byte chunk
    clientSocket.send(chunk)

# Receive response that can come in 64 byte chunks
response_data = b''

while True:
    # Receive a 64 byte chunk
    chunk = clientSocket.recv(64)

    # If there are no more 64 byte chunks left to receive
    if not chunk:
        break

    # Add up chunks to form complete message
    response_data += chunk

    # Check if we have at least the length prefix
    if len(response_data) >= n:
        # Get the length of the message that is given as the first n bytes
        expected_len = int(response_data[:n].decode())

        # Check if we have the complete message
        if len(response_data) >= expected_len + n:
            break

modifiedSentence = response_data[:expected_len + n]
print('From Server:', modifiedSentence[n:].decode())

clientSocket.close()
