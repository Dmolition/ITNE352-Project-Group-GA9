import json
import socket
import requests
import threading


# Function to handle client connection    part 4 threading function
def handle_client(client_socket, client_name):
    print("Accepted connection from", client_name)

    # Receive and process client requests
    while True:
        request = client_socket.recv(1024).decode('ascii')
        if not request:
            break
        # Parse client request
        request_parts = request.split(':')
        request_type = request_parts[0]
        request_params = request_parts[1:]

        # Perform the requested action and send response
        if request_type == '1':
            print(" Requester name: ",client_name ,"\n", "Type of request: All Arrived Flights","\n", "Request parameters: null")
            response = get_all_arrived_flights()
        elif request_type == '2':
            print(" Requester name: ",client_name ,"\n", "Type of request: All Delayed Flights","\n", "Request parameters: null")
            response = get_all_delayed_flights()
        elif request_type == '3':
            para = client_socket.recv(1024).decode('ascii')
            print(" Requester name: ",client_name ,"\n", "Type of request: All Flights from Specific Airport","\n", "Request parameters:{}".format(para))
            response = get_flights_from_airport(para)
        elif request_type == '4':
            para = client_socket.recv(1024).decode('ascii')
            print(" Requester name: ",client_name ,"\n", "Type of request: Details of Specific Flight","\n", "Request parameters:{}".format(para))
            response = get_flight_details(para)
        else:
            response = "Invalid request"

        # Send response to the client
        client_socket.send(response.encode('ascii'))

    # Close the connection
    print("Client", client_name, "disconnected")
    client_socket.close()

# Function to get all arrived flights
def get_all_arrived_flights():
    # Retrieve flight records from JSON file
    with open('group_GA9.json', 'r') as file:
        data = json.load(file)

    # Extract relevant flight information
    flights = data['data']
    arrived_flights = []
    for flight in flights:
        if flight['arrival']['estimated'] is not None:
            arrived_flight = {
                'Flight IATA Code': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Arrival Time': flight['arrival']['estimated'],
                'Arrival Terminal Number': flight['arrival']['terminal'],
                'Arrival Gate': flight['arrival']['gate']
            }
            arrived_flights.append(arrived_flight)

    return json.dumps(arrived_flights, indent=3)

# Function to get all delayed flights
def get_all_delayed_flights():
    # Retrieve flight records from JSON file
    with open('group_GA9.json', 'r') as file:
        data = json.load(file)

    # Extract relevant flight information
    flights = data['data']
    delayed_flights = []
    for flight in flights:
        if flight['departure']['estimated'] is not None and flight['departure']['estimated'] > flight['departure']['scheduled']:
            delayed_flight = {
                'Flight IATA Code': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Original Departure Time': flight['departure']['scheduled'],
                'Estimated Arrival Time': flight['arrival']['estimated'],
                'Arrival Terminal Number': flight['arrival']['terminal'],
                'Delay': flight['departure']['estimated'] - flight['departure']['scheduled'],
                'Arrival Gate': flight['arrival']['gate']
            }
            delayed_flights.append(delayed_flight)

    return json.dumps(delayed_flights, indent=3)

# Function to get flights from a specific airport
def get_flights_from_airport(airport_icao):
    # Retrieve flight records from JSON file
    with open('group_GA9.json', 'r') as file:
        data = json.load(file)

    # Extract relevant flight information
    flights = data['data']
    airport_flights = []
    for flight in flights:
        if flight['departure']['airport'] == airport_icao:
            airport_flight = {
                'Flight IATA Code': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Original Departure Time': flight['departure']['estimated'],
                'Estimated Arrival Time': flight['arrival']['estimated'],
                'Departure Gate': flight['departure']['gate'],
                'Arrival Gate': flight['arrival']['gate'],
                'Status': flight['flight_status']
            }
            airport_flights.append(airport_flight)

    return json.dumps(airport_flights, indent=3)

# Function to get details of a particular flight          part5
def get_flight_details(flight_iata):
    # Retrieve flight records from JSON file
    with open('group_GA9.json', 'r') as file:
        data = json.load(file)

    # Find the matching flight
    flights = data['data']
    for flight in flights:
        if flight['flight']['iata'] == flight_iata:
            flight_details = {
                'Flight IATA Code': flight['flight']['iata'],
                'Departure Airport': flight['departure']['airport'],
                'Departure Gate': flight['departure']['gate'],
                'Departure Terminal': flight['departure']['terminal'],
                'Arrival Airport': flight['arrival']['airport'],
                'Arrival Gate': flight['arrival']['gate'],
                'Arrival Terminal': flight['arrival']['terminal'],
                'Status': flight['flight_status'],
                'Scheduled Departure Time': flight['departure']['scheduled'],
                'Scheduled Arrival Time': flight['arrival']['scheduled']
            }
            return json.dumps(flight_details, indent=3)

    return "Flight not found"
 

# Main server code
def server():
    # Prompt user for airport code
    airport_code = input("Enter the airport code: ")

    # Set up API request parameters
    params = {
        'access_key': '53a8cce17762fffeb80bba61f11e573a',
        'arr_icao': airport_code,
        'limit': 100
    }

    # Send GET request to AviationStack API
    api_url = 'http://api.aviationstack.com/v1/flights'
    apiResponse = requests.get(api_url, params)

    # Process the response
    if apiResponse.status_code == 200:
        data = apiResponse.json()  # convert to json

        # Store the data in a JSON file
        file_path = 'group_GA9.json'
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=3)

        print("Flight records saved to", file_path)
    else:
        print("Error occurred:", apiResponse.status_code)

    # Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 4444)
    server_socket.bind(server_address)
    server_socket.listen(3)
    print("Server started. Listening for connections...")

    # Handle client connections
    while True:
        client_socket, client_address = server_socket.accept()

        # Receive client name
        client_name = client_socket.recv(1024).decode('utf-8')

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_thread.start()

# Start the server
server()
