import time
import uuid
from socket import *
import threading
import json

# TODO: Delimiter when serializing a Message object to JSON is '\n'


class Message:
    # The message class allows for each node to send a message to its neighbor with a uuid and flag
    # The node message when a leader is found should update its flag and tell the next node who the leader is.

    def __init__(self, uuid_val, flag):
        self.uuid = str(uuid_val)
        self.flag = flag

    # Make a json
    def to_json(self):
        return json.dumps({"uuid": self.uuid, "flag": self.flag})

    @staticmethod
    def from_json(data):
        obj = json.loads(data)
        return Message(obj["uuid"], obj["flag"])


class Node:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.state = 0

        self.my_ip = None
        self.my_port = None
        self.peer_ip = None
        self.peer_port = None

        self.peer_connection = None
        self.server_connection = None

        self.leader_id = None
        self.lock = threading.Lock()
        self.config_file = "a3/instance-2/config.txt"
        self.log_file = "a3/logs/log2.txt"  # Added missing log_file attribute

        # Load config when object is made
        self.config()

    # Function to read the config file with IP addresses and ports
    def config(self):
        try:
            with open(self.config_file, 'r') as file:
                lines = file.readlines()

                # Set my ip and port as the first line in the document delimited by a comma
                self.my_ip, self.my_port = lines[0].strip().split(',')
                self.my_port = int(self.my_port)

                # Get the next peer's ip and port
                self.peer_ip, self.peer_port = lines[1].strip().split(',')
                self.peer_port = int(self.peer_port)
        except Exception as e:
            print("There was an error loading the config file: " + self.config_file)
            print(f"Error: {e}")

    def log(self, message):
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"{message}\n")
        except Exception as e:
            print(f"Cannot write to log: {e}")

    def node_server(self):
        # Establish TCP socket
        server_socket = socket(AF_INET, SOCK_STREAM)
        # Set the port according to the first line in the config file
        server_socket.bind(('', self.my_port))

        # Await a connection to peer
        server_socket.listen(1)
        print(f"log listening on {self.my_ip}:{self.my_port}")

        peer_socket, peer_address = server_socket.accept()
        print(f"New connection from {peer_address}")

        # Store peer connection
        self.peer_connection = peer_socket

    def receive_peer(self):
        time.sleep(2)

        # Save peer socket connection to variable
        self.peer_connection = socket(AF_INET, SOCK_STREAM)

        while True:
            try:
                # Connect to peer socket using peer ip and port provided in config file
                self.peer_connection.connect((self.peer_ip, self.peer_port))

                print(f"Connected to peer at {self.peer_ip}:{self.peer_port}")

                # Exit loop on successful connection
                break
            except Exception as e:
                print(f"Connection failed: {e}")
                time.sleep(1)

        # Send message with flag 0
        self.send(Message(self.uuid, 0))

    def send(self, message_object):
        if self.peer_connection:
            try:
                self.peer_connection.sendall(
                    (message_object.to_json() + '\n').encode())

                print(
                    f"Sent: uuid={message_object.uuid}, flag={message_object.flag}")
            except Exception as e:
                print(f"Failed to send: {e}")


n = Node()
print(f"Node created with UUID: {n.uuid}")
print(f"My config: {n.my_ip}:{n.my_port}")
print(f"Peer config: {n.peer_ip}:{n.peer_port}")
