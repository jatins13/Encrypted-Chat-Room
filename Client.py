# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import base64 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 4: 
    print("Correct usage: script, IP address, port number, user ID")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
userId = str(sys.argv[3])
server.send(userId.encode())
server_resp = server.recv(1024)
server_resp = server_resp.decode()
# Vigenère cipher 
  
# Function to encode 
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
  
while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 
  
    """ There are two possible input situations. Either the 
    user wants to give  manual input to send to other people, 
    or the server is sending a message  to be printed on the 
    screen. Select returns from sockets_list, the stream that 
    is reader for input. So for example, if the server wants 
    to send a message, then the if condition will hold true 
    below.If the user wants to send a message, the else 
    condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(1024)
            message = message.decode()
            print(decoder("vigenerecipher",message)) 
        else: 
            message = sys.stdin.readline() 
            msg = message
            msg  = encoder("vigenerecipher",msg)
            server.send(msg.encode()) 
            sys.stdout.write("<You>")
            sys.stdout.write(message) 
            sys.stdout.flush() 
server.close()  
