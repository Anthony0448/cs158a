from socket import *
import threading

# TODO: YOU NEED THEM THREADS TO ALLOW SOCKETS TO BE ACCEPTED AND CONTINUE TO RECEIVE MESSAGES


class ChatServer:
    def __init__(self, host='localhost', port=12000):
        self.host = host
        self.port = port
        self.clients = {}
        self.server_socket = None

    def connect_to_server(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.port))

        # Listen for incoming connections
        self.server_socket.listen(25)

        print(f"Server listening on {self.host}':'{self.port}")

        # Keep listening and accept
        while True:
            # Throughout this loop, the server will continue to listen for new connections
            # Each loop will accept a new connection and store it in the clients dictionary
            # A server socket returns the socket and address as a tuple, so two variables are used to store them
            client_socket, client_address = self.server_socket.accept()

            # Store client in dictionary while using the port as the key to identify the client
            # client_address[1] is a client port
            self.clients[client_address[1]] = client_socket

            print(f"New connection from {client_address}")

            # Start a new thread to manage the client
            # Manage client is the function that will be called within the thread
            # client_socket is the socket object for the client
            # client_address[1] holds the port number of the client
            client_thread = threading.Thread(
                target=self.receive_client,
                args=(client_socket, client_address[1])
            )

            # Start thread so that the server can continue to listen for new connections while managing the client
            # The concurrency allows the server to manage multiple clients at the same time
            client_thread.start()

    # This function manages the client connection
    def receive_client(self, client_socket, sender_port):
        try:
            while True:
                # Receive message from client with a buffer of 1024
                message = client_socket.recv(1024).decode()

                # Check if client wants to exit
                if message.strip().lower() == "exit":
                    break

                # Print message on the server console
                print(f"{sender_port}: {message}")

                # Relay message to all other clients
                self.broadcast(sender_port, message)
        except socket.error:
            pass
        finally:
            # Remove client from list and close connection
            self.remove_client_dictionary(sender_port, client_socket)

    # Port is passed for dictionary
    def broadcast(self, sender_port, message):
        for i in self.clients.items():
            recipient_port = i[0]
            client_socket = i[1]

            # Send message to all clients except the sender (sender_port)
            if recipient_port != sender_port:
                try:
                    client_socket.send((f"{sender_port}: " + message).encode())
                except socket.error:
                    self.remove_client_dictionary(
                        recipient_port, client_socket)

    # Remove client from dictionary and close connection
    def remove_client_dictionary(self, disconnected_port, client_socket):
        # if disconnected_port is in the dictionary remove it and close the connection
        if disconnected_port in self.clients:
            del self.clients[disconnected_port]

            # Close connection
            client_socket.close()

            print(f"Client {disconnected_port} disconnected")


server = ChatServer()
server.connect_to_server()
