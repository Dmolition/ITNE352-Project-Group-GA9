import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('127.0.0.1', 4444)
client_socket.connect(server_address)

# Send client name to the server
client_name = input("Enter your name: ")
client_socket.send(client_name.encode('ascii'))

while True:
    # Prompt user for request option
    print("\nRequest Options:")
    print("1. Get all arrived flights")
    print("2. Get all delayed flights")
    print("3. Get flights from a specific airport")
    print("4. Get details of a particular flight")
    print("5. Quit")
    request_option = input("Enter request option (1-4) or '5' to quit: ")

    # Send request option to the server
    client_socket.send(request_option.encode('ascii'))

    # Handle the response from the server
    response = client_socket.recv(4096).decode('ascii')
    print("Server Response:")
    print(response)

    if request_option == '3':
     city= input("Which city are flights coming from: ")  
     client_socket.send(city.encode("ascii"))     

    if request_option == '4':
     city= input("Enter the flight number: ")  
     client_socket.send(city.encode("ascii"))   

    # Check if the client chose to quit
    if request_option == '5':
        break
    
  


# Close the connection
client_socket.close()