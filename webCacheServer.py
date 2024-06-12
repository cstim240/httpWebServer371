# This implementation use multi-threading to handle multiple client
# requests in parallel. This is achieved by creating a new thread
# for each incoming client connection.

import socket
import threading

proxyHost = '127.0.0.1'
proxyPort = 8081

# Function to handle incoming proxy requests
def handle_proxy_request(client_socket):
    # Receive
    request = client_socket.recv(2048).decode()
    print("Received request at proxy:")
    print(request)

    try:
        # Create a new socket to connect to the actual server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(('127.0.0.1', 12000))  # Connect to the actual web server
        server_socket.sendall(request.encode())  # Forward the client's request to the web server

        # Receive the response
        response = server_socket.recv(4096)
        server_socket.close() 

        # Send the response back to the client
        client_socket.sendall(response)
    except Exception as e:
        # If an error occurs, print it and send an internal server error response to the client
        print(f"Error: {e}")
        response = 'HTTP/1.1 500 Internal Server Error\n\n'
        client_socket.send(response.encode())
    
    # Close the client socket
    client_socket.close()

# Start the proxy server
def start_proxy():
    # Create a socket for the proxy server
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxyHost, proxyPort))
    proxy_socket.listen(5)  
    print(f"Proxy server started at {proxyHost}:{proxyPort}")

    #this allows the proxy server to handle multiple client requests in parallel 
    while True:
        client_socket, addr = proxy_socket.accept()  # Accept a connection from a client
        # Create a new thread to handle the client's request
        client_handler = threading.Thread(target=handle_proxy_request, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()
