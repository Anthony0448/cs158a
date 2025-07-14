import time
import uuid
from socket import *
import threading
import json


class Message:
    # The message class allows for each node to send a message to its neighbor with a uuid and flag
    # The node message when a leader is found should update its flag and tell the next node who the leader is.

    def __init__(self, uuid_val, flag):
        self.uuid = str(uuid_val)
        self.flag = flag

    # Make a json
    def to_json(self):
        return json.dumps({"uuid": self.uuid, "flag": self.flag})

    # Make a message from json
    # It is static because it doesn't need to be an instance of the Message class to be called
    @staticmethod
    def from_json(data):
        obj = json.loads(data)
        return Message(obj["uuid"], obj["flag"])


class Node:
    # The main class for the node that handles the server and client connections
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.state = 0

        self.my_ip = None
        self.my_port = None
        self.peer_ip = None
        self.peer_port = None

        # The incoming connection is the socket that the server accepts for receiving messages
        self.incoming_connection = None
        # The outgoing connection is the socket that the client connects for sending messages
        self.outgoing_connection = None

        self.leader_id = None
        self.lock = threading.Lock()
        self.config_file = "config.txt"
        self.log_file = "log1.txt"  # Added missing log_file attribute

        # Load config when object is made by calling the config function
        self.config()

    # Function to read the config file with IP addresses and ports
    def config(self):
        try:
            with open(self.config_file, 'r') as file:
                lines = file.readlines()

                # Set my ip and port as the first line in the document delimited by a comma
                # strip() removes whitespace
                self.my_ip, self.my_port = lines[0].strip().split(',')
                # Convert port to int to be used in the server socket
                self.my_port = int(self.my_port)

                # Get the next peer's ip and port
                # Comma delimiter
                self.peer_ip, self.peer_port = lines[1].strip().split(',')
                self.peer_port = int(self.peer_port)
        except Exception as e:
            print("There was an error loading the config file: " +
                  self.config_file + " " + str(e))

    # Function to write to log file
    def log(self, message):
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"{message}\n")
        except Exception as e:
            print(f"Cannot write to log: {e}")

    # Function to start the server
    def node_server(self):
        # Establish TCP socket
        server_socket = socket(AF_INET, SOCK_STREAM)
        # Set the port according to the first line in the config file
        server_socket.bind(('', self.my_port))

        # Await a single connection to peer node
        server_socket.listen(1)
        print(f"Listening on {self.my_ip}:{self.my_port}")

        # Accept connection to peer node
        peer_socket, peer_address = server_socket.accept()
        print(f"New connection from {peer_address}")

        # Store peer socket connection to variable
        self.incoming_connection = peer_socket

        # Receive message from peer
        self.receive_messages(peer_socket)

    # Function to receive and process messages from peer
    def receive_messages(self, peer_socket):
        # The buffer is a string that stores the received data as it is received
        buffer = ""

        # Loop to receive messages from peer until the connection is closed
        while True:
            try:
                # Receive data from peer the socket (We are in loop so this will keep receiving till message finishes)
                data = peer_socket.recv(1024).decode()

                # Break loop if there's no data
                if (not data):
                    break

                # Continuously build the string of data received from peer
                buffer += data

                # While there exists a new line character, keep receiving the message
                # The \n is used to indicate the end of the message
                while '\n' in buffer:
                    message_str, buffer = buffer.split('\n', 1)

                    # If the message is not empty, create a Message object from the string
                    if message_str.strip():
                        message = Message.from_json(message_str.strip())

                        # Convert the uuid string to a UUID object
                        received_uuid = uuid.UUID(message.uuid)

                        # If received is greater, that uuid should be forwarded to the next node
                        if (received_uuid > self.uuid):
                            comparison = "greater"
                        # If equal, the uuid came back to the node meaning it should be the leader and is the largest
                        elif (received_uuid == self.uuid):
                            comparison = "same"
                        # Current node has a uuid larger than the one it received, so pass its own uuid forward
                        else:
                            comparison = "less"

                        state_info = f"{self.state}"
                        if (self.state == 1 and self.leader_id):
                            state_info += f" (leader: {self.leader_id})"

                        print(
                            f"Received: uuid={message.uuid}, flag={message.flag}, {comparison}, {state_info}")
                        self.log(
                            f"Received: uuid={message.uuid}, flag={message.flag}, {comparison}, {state_info}")

                        match message.flag:
                            # Case zero meaning a leader has not been selected, yet
                            case 0:
                                # If the same received uuid matches current Node, then it looped back here determining it is the largest
                                if (comparison == "same"):
                                    # Set leader uuid to current Node.
                                    # Let other nodes know a leader was found
                                    self.leader_id = self.uuid

                                    # A state of 1 means a leader has been found
                                    self.state = 1

                                    # Log the found leader uuid
                                    print(
                                        f"Leader is decided to {self.leader_id}")
                                    self.log(
                                        f"Leader is decided to {self.leader_id}")

                                    # Forward current Node's uuid to the peer (leader uuid)
                                    # Send message that the flag is 1 because a leader was found
                                    self.send(Message(self.uuid, 1))
                                elif (comparison == "greater"):
                                    # If the received uuid was greater than current Node, forward that uuid instead of its own
                                    self.send(Message(received_uuid, 0))
                                else:
                                    # If the current node has a greater uuid, then forward its own UUID and ignore received message
                                    # Send own message
                                    self.log(
                                        f"Received message ignored. Forward own UUID: {self.uuid}")
                                    self.send(Message(self.uuid, 0))
                            case 1:
                                # If a leader has already been selected
                                if (self.state == 0):
                                    self.leader_id = received_uuid
                                    self.state = 1

                                    print(
                                        f"Leader is decided to {self.leader_id}")
                                    self.log(
                                        f"Leader is decided to {self.leader_id}")

                                    # Send forward the message of leader found
                                    self.send(message)
                                elif (self.leader_id == received_uuid):
                                    # Stop the passing of leader announcement
                                    print("Election complete")
                                    self.log("Election complete")

                                    return
                                else:
                                    # Forward announcement
                                    self.send(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    # Function to connect to peer node
    def receive_peer(self):
        # Wait for 2 seconds before connecting to peer to ensure server is ready
        time.sleep(2)

        # Save peer socket connection to variable
        self.outgoing_connection = socket(AF_INET, SOCK_STREAM)

        # Loop to connect to peer until successful
        while True:
            try:
                # Connect to peer socket using peer ip and port provided in config file
                self.outgoing_connection.connect(
                    (self.peer_ip, self.peer_port))

                print(f"Connected to peer at {self.peer_ip}:{self.peer_port}")

                # Exit loop on successful connection
                break
            except Exception as e:
                print(f"Connection failed: {e}")

                # Wait 1 second before trying again
                time.sleep(1)

        # Send message with flag 0 because no leader has been found yet
        self.send(Message(self.uuid, 0))

    # Function to send message to peer using passed Message object
    def send(self, message_object):
        # Use outgoing_connection to send messages to the next node in the ring
        # Outgoing connection is the socket that the client connects for sending messages
        if self.outgoing_connection:
            try:
                # Send message to peer. sendall is used to send the entire message in one go
                # The \n is used to indicate the end of the message
                self.outgoing_connection.sendall(
                    (message_object.to_json() + '\n').encode())

                print(
                    f"Sent: uuid={message_object.uuid}, flag={message_object.flag}")
                self.log(
                    f"Sent: uuid={message_object.uuid}, flag={message_object.flag}")
            except Exception as e:
                print(f"Failed to send: {e}")
        else:
            print("No outgoing connections :(")


n = Node()

print(f"Node created with UUID: {n.uuid}")
print(f"My config: {n.my_ip}:{n.my_port}")
print(f"Peer config: {n.peer_ip}:{n.peer_port}" + '\n')


# Start the server in a separate thread to allow for concurrent connections
# Use the node_server function to start the server
server_thread = threading.Thread(target=n.node_server)
# The daemon closes the thread when the code finishes/stops
server_thread.daemon = True
server_thread.start()

# Start the client to connect to peer in a separate thread to allow for concurrent connections
client_thread = threading.Thread(target=n.receive_peer)
client_thread.daemon = True
client_thread.start()

# Keep main running continously to keep the server alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")