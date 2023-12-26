import socket
from tkinter import *
from tkinter import ttk




# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = (('127.0.0.1', 4444))
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
    if request_option == '1':
       print("Arrived flights information")
    if request_option == '2':
        print("Delayed flights information")

    if request_option == '3':
     city= input("Which city are flights coming from: ")  
     client_socket.send(city.encode("ascii"))     

    if request_option == '4':
     city= input("Enter the flight number: ")  
     client_socket.send(city.encode("ascii"))   

    # Check if the client chose to quit
    if request_option == '5':
        break
    
    root=Tk()
    b1=ttk.Button(root,text="Get data")
    b1.pack()
    entry1=ttk.Entry(root,width=30)
    entry1.pack()

    def bClick():
       print(entry1.get())
    b1.config(command=bClick)

    style=ttk.style()
    style.theme_use('classic')
    ttk.Label(root,background='blue',text='black').grid(row=0,column=0,sticky='ew')
    ttk.Label(root,background='green',text='pink').grid(row=0,column=1,sticky='ew')
    ttk.Label(root,background='blue',text='green').grid(row=1,column=0,columnspan=2,sticky='ew')
    ttk.Label(root,background='brown',text='green').grid(row=0,column=2,rowspan=2,sticky='ew')
    root.rowconfigure(0,weight=1)
    root.rowconfigure(1,weight=1)
    root.columnconfigure(0,weight=1)
    root.columnconfigure(1,weight=1)
    root.columnconfigure(2,weight=1)

    username_entry=ttk.Entry(root)
    username_entry.grid(row=0,coulmn=1,columnspan=3)
    def connect():
       
     OptionSelect=StringVar()
     ToSelect=ttk.label(root,text='select the option please')
    S1=ttk.Radiobutton(root,text='A.Arrived flights',variable=OptionSelect,value='A',command=toggle_entry_state)
    S1=ttk.Radiobutton(root,text='B.Delayed flights',variable=OptionSelect,value='B',command=toggle_entry_state)
    S1=ttk.Radiobutton(root,text='C.flights from specific city',variable=OptionSelect,value='C',command=toggle_entry_state)
    S1=ttk.Radiobutton(root,text='D. details of a particular flights',variable=OptionSelect,value='D',command=toggle_entry_state)
     

    bRequest=ttk.Button(root,text='request',command=lambda:handle_connection(True))
    bQuit=ttk.Button(root,text='quit',command=destroy)
    bQuit.grid(row=3,column=1)


    root.mainloop()

# Close the connection
client_socket.close()