import socket

cacheSocket = socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket object
cachePort = 12001 #server port

server_address = ('localhost', cachePort)
cacheSocket.bind(server_address)

cacheSocket.listen(5) #listen for incoming connections, the 1 is the maximum number of queued connections
print("The cache server is ready to receive")

cache = {} #dictionary to store the cache

while True: 
    print("Waiting for incoming connection")
    connection, client_address = cacheSocket.accept() #accept the connection, tuple unpacking is used to assign different variables

    try: 
        print("Connection from", client_address)

        #receive the request, send response
        while True: 
            data = connection.recv(2048)
            print("Received: ", data)
            if data: 
                print("Sending data back to the client")
                connection.sendall(data)
            else: 
                print("No more data from", client_address)
                break
    finally:
        connection.close()
