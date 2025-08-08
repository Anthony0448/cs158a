from socket import *
from ssl import *

hostname = 'www.google.com'
hostport = 443
context = create_default_context()

# Make a secure connection to the server using
with create_connection((hostname, hostport)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print("SSL connection established")
        print(ssock.version())

        # \r and \n are needed to separate the HTML headers from the body
        http_request = (
            f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n")

        # Send GET request to the server
        ssock.send(http_request.encode('utf-8'))

        # A bytestring to store the response
        response = b""

        # While there is data to receive keep receiving it and add it to response
        while True:
            # Receive data from the server at 4096 bytes at a time
            data = ssock.recv(4096)

            # If there is no more data to receive break the loop
            if not data:
                break

            # Add the data to the response
            response += data

        # response is a bytestring so it should be decoded to a string
        response = response.decode('utf-8')

        # Split the response into headers and body
        # The 1 is used to split the response into two parts
        parts = response.split('\r\n\r\n', 1)

        # Use parts to separate the headers and the body, so the header is not included in the body
        headers, html_content = parts

        # Save HTML content to an html file
        with open("response.html", 'w', encoding='utf-8') as f:
            # Use html_content to write to the file instead of response because response includes the headers
            f.write(html_content)

        print("HTML content saved to response.html")
