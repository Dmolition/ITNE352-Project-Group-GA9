import socket
import json
socket_c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_c.connect(('127.0.0.1',4444))
print("client has been started")
#ask the client about the username
Username_c=input("enter the username please")
#the client send the username to  the server
socket_c.send(Username_c.encode('ascii'))
print("Select the option that you need please")
choices=input("Hello,which option you are looking for?")
while a != 0:
    print("\n 1.Arrived flight :")
    print("2.Delayed flights :")
    print("3.All flights coming from a specific city :")
    print("4.Details of particular flight :")
    print("5.Quit")
    a=input("Enter the option number\n")
    socket_c.sendto(a.encode('ascii'), ('127.0.0.1', 4444))

    if a == '1':
       print("Arrived flight :")

    elif a=='2':
        print("Delayed flights :")

    elif a=='3':
        City=input("which cities that the flights coming from?")
        print("All flights coming from a specific city : ",City)

    elif a=='4':
        fnumber=input("enter the flight number please")
        print("flights number ",fnumber)

    elif a == '5':
        print("quit the connection(disconnected)")
        break
    socket_c.close()