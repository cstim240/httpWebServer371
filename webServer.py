# Implement a simple web server able to process and respond to HTTP requests.
# Should be able to respond to the requests with the following messages for the relevant HTTP status codes: 200, 304, 400, 403, 404
# So for each item, you need to decide what are the requirements in the request, what method is used, and what part of the message is 
# causing the specified status code in the response.
# NOT ALLOWED TO USE Python HTTP module or any other module that does the work for you.

# Step 1 - Determine Requirements
# 200 (OK) indicates the request was successful - payload returned. GET method is used to request the resource.
# Methods used: (GET, POST, PUT, DELETE, OPTIONS, TRACE)
# Part of msg causing 200: Request line, headers, body

#304 (Not Modified) indicates the client has the response in its cache. Indicates a conditional GET or HEAD request 
# has been received, would've resulted in 200 response if not for the fact that the condition evaluated to false.
# no needs for a server to transfer a representation of the target resource because the client already has a valid representation.
# Methods used: (GET, HEAD)
# Part of msg causing 304: cache-control, conttent-location, date, etag, expires, and vary are some of the headers that can cause 304

#400(Bad Request) indicates the server cannot/will not process request due to client error.
# error could be malformed request syntax, invalid request message framing, depetive request routing
# Methods used: (GET, POST, PUT, DELETE, OPTIONS, TRACE)
# Part of msg causing 400: Request line, headers, body

#403(Forbidden) indicates the server understood request but refuses to authorize it. 
# client does not have permission to access the requested resource.
# Methods used: (GET, POST, PUT, DELETE, OPTIONS, TRACE)
# Part of msg causing 403: Request line, headers, body

#404(Not Found) indicates the server can't find the requested resource
# Methods used: (GET, POST, PUT, DELETE, OPTIONS, TRACE)
# Part of msg causing 404: Request line, headers, body

#Write down the specifications of the logic for the generation of each of these status codes,
#and the HTTP request message you will use to test it.

#Step 2 - Design the server
from socket import * 
import os 
import threading

serverPort = 12000  # Server port

serverSocket = socket(AF_INET, SOCK_STREAM)  # Create a socket object
serverSocket.bind(('127.0.0.1', serverPort))  # Bind the socket to the host and port
serverSocket.listen(5)  # Listen for incoming connections, the 5 is the maximum number of queued connections
print("The server is ready to receive")  # Print a message to the console
print("Host name:" + gethostname())
valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE']  # List of valid methods
last_modified_times = {}


# Function to handle client requests
def handle_client(clientsocket):
    try:
        message = clientsocket.recv(2048).decode('utf-8')  # Receive the message from the client, decode it from bytes to a string
        print("From server:", message)  # Print the message to the console

        request_line = message.split('\n')[0]  # Split the message by the newline character
        request_method, path, version = request_line.split()  # Split the request line by the space character

        if request_method not in valid_methods:
            response = 'HTTP/1.1 400 Bad Request\n\n'  # Create response message for 400 status code
            clientsocket.send(response.encode('utf-8'))  # Send the response to the client
        elif request_method == 'GET':
            if path == '/userCreditCard.html':
                response = 'HTTP/1.1 403 Forbidden\n\n'
                clientsocket.send(response.encode('utf-8'))
            elif path == '/test.html':
                last_modified = os.path.getmtime('test.html')
                # Returns the time of last modification of the file specified in the path

                # If the path is in the dictionary and the last modified time is the same as the last modified time of the file
                if path in last_modified_times and last_modified_times[path] == last_modified:
                    response = 'HTTP/1.1 304 Not Modified\n\n'
                else:
                    with open('test.html', 'r') as file:  # Open the file in read mode
                        file_content = file.read()  # Read the content of the file
                    response = 'HTTP/1.1 200 OK\n\n' + file_content  # Create response message for 200 status code
                    last_modified_times[path] = last_modified
                clientsocket.send(response.encode('utf-8'))
            else:
                response = 'HTTP/1.1 404 Not Found\n\n'
                clientsocket.send(response.encode('utf-8'))

        clientsocket.close() # Close the socket after uses
    except Exception as e:
        print(f"Error: {e}")
        response = 'HTTP/1.1 500 Internal Server Error\n\n'
        clientsocket.send(response.encode('utf-8'))
        clientsocket.close()  # Ensure the connection is closed in case of an error


while True:
    clientsocket, address = serverSocket.accept()
    # Create a new thread to handle the client request, same as webCacheServer
    client_thread = threading.Thread(target=handle_client, args=(clientsocket,))
    client_thread.start()

    #use the commands below to run the server
    #python3 webServer.py

    #use the commands below to test the server on a different terminal
    #curl -i http://localhost:12000/test.html for an OK response
    #curl -i http://localhost:12000/test.html again for a Not Modified response
    #curl -i http://localhost:12000/userCreditCard.html for a Forbidden response
    #curl -i http://localhost:12000/invalid.html for a Not Found response
    #curl -i -X INVALID http://localhost:12000/ for a Bad Request response, by default curl uses the GET method
    # the -X flag is used to specify the method to be used

    #Try on a browser: http://192.168.1.70:12000/test.html for a 200 response which will load the test.html file
    #http://192.168.1.70:12000/userCreditCard.html for a 403 response which will display a Forbidden message

#Step 3: Performance
#(a) Think about a web proxy server. What is different in request handling in a proxy server and a web server that hosts your files?
#Based on the class' module 2 slides 29-34, a web proxy server/web cache is a server that sits between a client and a web server.
#Cache acts as both client and server. It's the middle man which acs as a server for the client and a client for the server.
# This reduces the response time for client requests and reduce traffic on an institution's access link. 
# The proxy server stores copies of the resources that have been requested by clients.


#Step 4
# With multithreading, the server can handle multiple request concurrently
# reducing the likelihood of HOL blocking.

