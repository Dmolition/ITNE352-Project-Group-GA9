import re
import hashlib
import socket
import sqlite3
import time
import sys

# Regular expression pattern for username validation
username_pattern = r"^(?=.*[A-Z])(?=.*\d{2})[a-zA-Z\d]{8,}$"

# Function to create and initialize the user database
def initialize_user_database():
    conn = sqlite3.connect('user_database.sqlite')
    c = conn.cursor()

    # Create the user table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password_hash TEXT)''')

    # Insert sample data
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ('Johndd99', 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86'))
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ('AliceSm12', 'ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413'))
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ('BobJoh23', '54c8e9ed836eb9622f6694876dabd83e44c6f7ce11cb97c9be368eaac9edc7cd3b8a78888129018ec4bdf2a2d4d83c6b7cae722c22615e9e1cf309c3e3e12ad2'))
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", ('Mehmet87', 'bf88d23949f70225690a77c50974f48b5504cc8da2aef87b646af1e094b040ce7b08e67179a63eda12b5aacb85cb5f6280475f7ef295cf56b1fe05f54e8dad5a'))

    conn.commit()
    conn.close()

# Function to retrieve user database from the database file
def load_user_database():
    conn = sqlite3.connect('user_database.sqlite')
    c = conn.cursor()

    user_database = {}
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    for row in rows:
        username, password_hash = row
        user_database[username] = password_hash

    conn.close()
    return user_database

# Wait for the server to be online
server_address = ('127.0.0.1', 4444)
connected = False
while not connected:
    try:
        # Try to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        connected = True
    except ConnectionRefusedError:
        # Connection refused, server is not online yet
        print("Server is not online. Retrying in 4 seconds...")
        time.sleep(4)

print("Connected to the server.")

# Initialize the user database (only needed once)
initialize_user_database()

# Load user database from the database file
user_database = load_user_database()

# Send client name and password hash to the server
while True:
    try:
        client_name = input("Enter Username: ")
        password = input("Enter Password: ")

        if re.match(username_pattern, client_name):
            if (
                client_name in user_database and hashlib.sha512(password.encode()).hexdigest() == user_database[client_name]
            ):
                break
            else:
                print("Invalid username or password. Please try again.")
        else:
            print("Invalid username format. Please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(0)

client_socket.send(client_name.encode('ascii'))


# Main loop for sending requests
while True:
    try:
        # Prompt user for request option
        print("\nRequest Options:😄")
        print("1. Get all arrived flights😄")
        print("2. Get all delayed flights😌 ")
        print("3. Get flights from a specific airport😄")
        print("4. Get details of a particular flight😄")
        print("5. Quit😢") 
    
        request_option = input("Enter request option (1-4) or '5' to quit: ")

        # Send request option to the server
        client_socket.send(request_option.encode('ascii'))

        if request_option == '1':
            pass
        
        elif request_option == '2':
            pass

        elif request_option == '3':
            sAirportpara = input("Which city are flights coming from: ")
            client_socket.send(sAirportpara.encode('ascii'))
        
        elif request_option == '4':
            sFlightpara = input("Enter the flight IATA: ")
            client_socket.send(sFlightpara.encode('ascii'))
        
        # Check if the client chose to quit
        elif request_option == '5':
            # Receive and print the response from the server
            print(f"{client_name} disconnected")
            break

        # Handle the response from the server
        response = client_socket.recv(4096).decode('ascii')
        print("Server Response:")
        print(response)

    except ConnectionResetError:
        print("The connection with the server was reset. Please try again.")
    
    except KeyboardInterrupt:
        print("\nProgram forcelly stopped by user. Exiting...")
        sys.exit(0)

    except Exception as e:
        print("An error occurred:", str(e))

# Close the connection
client_socket.close()