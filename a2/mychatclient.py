from socket import *
import threading


class ChatClientUser:
    # Built in function that is always executed when object is made
    def __init__(self, host='localhost', port=12000):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False

    # Pass self (self reference instance)
    def connect_to_server(self):
        # Connect to the chat server
        try:
            # TCP
            self.client_socket = socket(AF_INET, SOCK_STREAM)

            # Connect to server using instance variables
            self.client_socket.connect((self.host, self.port))

            # Change state to running when connection is established
            self.running = True

            print("Connected to chat server. Type 'exit' to close connection.")

            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            # Make thread daemon so it exits when main thread exits (an error happens without this...)
            receive_thread.daemon = True
            receive_thread.start()

            # Start sending messages from main thread
            # Will not trigger disconnect until this ends
            self.send_messages()

        except socket.error as e:
            print(f"Failed to connect to server: {e}")
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        # Always end is a disconnect
        finally:
            self.disconnect()

    def receive_messages(self):
        # Receive messages from the server
        while self.running:
            try:
                # Receive buffer of 1024
                message = self.client_socket.recv(1024).decode()

                # If there's a message
                if message:
                    print(message)
                else:
                    # No message no loop
                    break
            except socket.error:
                break

        self.running = False

    # Send messages to the server
    def send_messages(self):
        # So long as the client is considered to be running, stay connected
        while self.running:
            try:
                message = input()

                # If the message is exit then close connection
                if message.strip().lower() == 'exit':
                    # Send message to server to exit
                    self.client_socket.send(message.encode())

                    # Exit loop
                    break

                # Send message to server
                self.client_socket.send(message.encode())

            except KeyboardInterrupt:
                break
            except socket.error:
                break

        # If the loop is no longer running, the client is not connected.
        self.running = False

    # Disconnect from the server
    def disconnect(self):
        # Disconnected from the server so set running to false
        self.running = False

        # If the socket connection exists, close it
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                # If the socket connection is not closed then pass
                pass

        print("Disconnected from server")


# Make instance of ChatClientUser
client = ChatClientUser()
client.connect_to_server()
