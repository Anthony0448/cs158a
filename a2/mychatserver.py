from socket import *
import threading

# TODO: YOU NEED THEM THREADS TO ALLOW SOCKETS TO BE ACCEPTED AND CONTINUE TO RECEIVE MESSAGES


class ChatServer:
    def __init__(self, host='localhost', port=12000):
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to store client connections {port: socket}
        self.server_socket = None

    def connect_to_server(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.port))

        # Listen for incoming connections
        self.server_socket.listen(25)

        print(f"Server listening on {self.host}':'{self.port}")

        # Keep listening and accept
        while True:
            client_socket, client_address = self.server_socket.accept()

            print(f"New connection from {client_address}")

            # Start a new thread to manage the client
            # client_address[1] holds the port number of the client
            client_thread = threading.Thread(
                target=self.manage_client,
                args=(client_socket, client_address[1])
            )
            # Start thread so that the server can continue to listen for new connections while managing the client
            # The concurrency allows the server to manage multiple clients at the same time
            client_thread.start()

    # This function manages the client connection
    def manage_client(self, client_socket, client_port):
        try:
            while True:
                # Receive message from client
                message = client_socket.recv(1024).decode()

                # Check if client wants to exit
                if message.strip().lower() == "exit":
                    break

                # Print message on the server console
                print(f"{client_port}: {message}")
        except socket.error:
            pass


server = ChatServer()
server.connect_to_server()
