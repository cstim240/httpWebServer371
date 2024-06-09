# Implement a simple web server able to process and respond to HTTP requests.
# Should be able to respond to the requests with the following messages for the relevant HTTP status codes: 200, 304, 400, 403, 404
# So for each item, you need to decide what are the requirements in the request, what method is used, and what part of the message is 
# causing the specified status code in the response.
# NOT ALLOWED TO USE Python HTTP module or any other module that does the work for you.

# Part 1 - Determine Requirements
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

from socket import * #this module provides access to the BSD socket interface

serverName = 'localhost' #server name
serverPort = 12000 #server port

serverSocket = socket(AF_INET, SOCK_STREAM) #create a socket object
serverSocket.bind((gethostname(), serverPort)) #bind the socket to the host and port
serverSocket.listen(1) #listen for incoming connections, the 1 is the maximum number of queued connections 
print("The server is ready to receive") #print a message to the console

while True:
    clientsocket, address = serverSocket.accept() #accept the connection, tuple unpacking is used to assign different variables
    #to the different parts of the tuple, in this case the accept method returns a tuple with the client socket and the address
    message = clientsocket.recv(2048).decode('utf-8') #receive the message from the client, decode it from bytes to a string
    #the input parameter of recv specifies the maximum amount of data to be received at once, in this case 2048 bytes
    print("From server:", message) #print the message to the console

    request_line = message.split('\n')[0] #split the message by the carriage return and newline characters
    request_method, path, version = request_line.split() #split the request line by the space character

    if request_method == 'GET':
        if path == '/userCreditCard.html':
            response = 'HTTP/1.1 403 Forbidden\n\nAccess to this resource is forbidden'
            clientsocket.send(response.encode('utf-8')) #send the response to the client
            print('Forbidden access to userCreditCard.html') #handle the request for userCreditCard.html
        elif path == '/test.html':
            print('Received request for test.html') #handle the request for test.html
        else: 
            print('Received request for another file') #handle other paths



