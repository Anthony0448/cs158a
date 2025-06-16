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
    if len(original_sentence) >= n and original_sentence[:n].isdigit():
        byte_size = int(original_sentence[:n])

        print(f"Byte size: {byte_size}")

        break
    else:
        print(
            f"Invalid input. The first {n} characters must be digits. Please try again.")


encoded_original_sentence = original_sentence.encode()

# Send message in chunks of 64 (buffsize 64)
# Increment up to encoded sentence length by 64 each loop
for i in range(0, len(encoded_original_sentence), 64):
    # Extract bytes from i to (i + 64) ; Like take bytes from 0 to 0 + 64 then 64 to 128
    chunk = encoded_original_sentence[i:i+64]

    # Send each 64 byte chunk
    clientSocket.send(chunk)


# Buffersize is 64
modifiedSentence = clientSocket.recv(64)

print('From Server:', modifiedSentence.decode())

clientSocket.close()
