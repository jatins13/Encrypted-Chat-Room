# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from _thread import *
import mysql.connector

cnx = mysql.connector.connect(user = 'root',password = 'MySql134*',
                            host = 'localhost', database='chatroom', auth_plugin = 'mysql_native_password')
    
cursor = cnx.cursor()

"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
  
# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 
  
# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 
  
#Binding the socket to the IP address and port number
server.bind((IP_address, Port)) 
  
server.listen(100) 
  
list_of_clients = [] 
  

def encoder(key, clear): 
    enc = [] 
      
    for i in range(len(clear)): 
        key_c = key[i % len(key)] 
        enc_c = chr((ord(clear[i]) +
                     ord(key_c)) % 256) 
                       
        enc.append(enc_c) 
       
    stri=""
    stri = stri.join(enc)    
    return stri

# Function to decode 
def decoder(key, enc): 
    dec = [] 
      
    
    for i in range(len(enc)): 
        key_c = key[i % len(key)] 
        dec_c = chr((256 + ord(enc[i]) -
                           ord(key_c)) % 256) 
                             
        dec.append(dec_c) 
    return "".join(dec) 
  
def clientthread(conn, addr, userName): 
  
    # sends a message to the client whose user object is conn 
    msg = "Welcome to this chatroom!"
    msg = encoder("vigenerecipher",msg)
    conn.send(msg.encode()) 
  
    while True: 
            try: 
                message = conn.recv(1024) 
                if message: 
  
                    """prints the message and address of the 
                    user who just sent the message on the server 
                    terminal"""
                    message = message.decode()
                    message = decoder("vigenerecipher",message)
                    print("<" + userName + "> " + message) 
  
                    # Calls broadcast function to send message to all
                    message = "<" + userName + "> " + message
                    message = encoder("vigenerecipher",message)
                    broadcast(message.encode(), conn) 
  
                else: 
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    remove(conn) 
  
            except: 
                print("Couldn't broadcast")
                continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
    
                # if the link is broken, we remove the client 
                remove(clients) 
  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept() 
    user_id = conn.recv(1024)
    user_id = int(user_id.decode())
    passe = ""
    query_name = ("SELECT * FROM chatroom_logins "
                "WHERE user_id = %s ")
    cursor.execute(query_name,(user_id,))
    userName = ""
    for(user_id,name,password) in cursor:
        # print("Hello {}, enter your password to enter IMF".format(name))
        passe = password
        userName = name
    if(len(userName)>0):
        server_resp = "Please enter your password."
        server_resp = server_resp.encode()
        conn.send(server_resp)
        passq = input()
        passq = str(passq)
        if(passq != passe):
            server_resp = "Password Incorrect"
            server_resp = server_resp.encode()
            conn.send(server_resp)
            conn.close()
        else:   
            server_resp = "Welcome to the chatroom!"
            server_resp = server_resp.encode()
            conn.send(server_resp)
            """Maintains a list of clients for ease of broadcasting 
            a message to all available people in the chatroom"""
            list_of_clients.append(conn) 
        
            # prints the address of the user that just connected 
            print (addr[0] + " connected")
        
            # creates and individual thread for every user  
            # that connects 
            start_new_thread(clientthread,(conn,addr, userName))  
    else:    
        server_resp = "Invalid user name"
        server_resp = server_resp.encode()
        conn.send(server_resp)
       
cursor.close()
cnx.close()
conn.close() 
server.close() 