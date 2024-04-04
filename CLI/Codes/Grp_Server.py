from socket import *
from AES import*
import json
import RSA
import threading,base64
import secrets
import string

info = {}
clients = []
addresses = []

def initialize_client():
    # initialize socket
    global private_key,conn
    s = socket(AF_INET, SOCK_STREAM)
    # config details of server
    host = input("Ip Address of the Server :")
    n = input("No of People :")  ## to use between devices in the same network eg.192.168.1.5
    port = 1234
    public_key, private_key = RSA.generate_keypair()
    session_key = ''.join(secrets.choice(string.ascii_letters) for _ in range(16))
    # initialize server
    s.bind((host, port))
    print("Server Established. Please Connect to the server for Chatting.\n")
    # set no. of clients
    s.listen(int(n))
    # accept the connection from client
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        addresses.append(addr)
        # Start a new thread to handle the client
        user_2 = conn.recv(1024).decode('utf-8')
        ds = json.loads(user_2)
        name = ds["user"]
        rsa = ds["rsa"]
        info[addr] = [name,rsa]
        if len(addresses)>1:
         se_in = ','.join(info[i][0] for i in addresses if i != addr)
         se_info = f'{se_in} Present in the chat.'
        else :
            se_info = "Welcome to the Chat. Waiting for people to connect."
        data_to_send = {'pub': public_key, 'key':RSA.RSA_encrypt(session_key,rsa),'s_info':se_info}

# Convert the data to a JSON string
        json_data = json.dumps(data_to_send)    
        conn.send(json_data.encode('utf-8'))
        a = f'{name} connected to the chat.'
        data_to_send = {'name': a, 'op':3}

# Convert the data to a JSON string
        json_data = json.dumps(data_to_send)     
        send(json_data.encode('utf-8'),conn)   

        client_handler = threading.Thread(target=receive, args=(conn, addr))
        client_handler.start()
def send(a,b):
        for client, address in zip(clients, addresses):
           try:
               if client!= b: 
                client.send(a)
           except:
                # Handle the case where a client is no longer reachable
                clients.remove(client)
                addresses.remove(address)

def receive(conn,addr):
 while 1:
    try:
            '''data = conn.recv(10240).decode('utf-8')
            ds = json.loads(data)'''
            datas = b""
            o=1
            while o!=0:
              data = conn.recv(1024)
              datas += data
              if datas[-1]==125:
                  o=0
                  break
            f_d = datas.decode('utf-8')
            f_d = json.loads(f_d)
            if f_d["op"]==0:
             msg = decrypt(f_d["data"],RSA.RSA_decrypt(f_d["rsa"],private_key))
             if msg != "":
                f_d["u"] = info[addr][0]
                f_d["data"] = msg
                datas_t =json.dumps(f_d)
                send(datas_t.encode('utf-8'),conn)
                print(f'{info[addr][0]} :'+msg)
                print("\n")
            else:
             print(f'{info[addr][0]} Sent a {f_d["ext"]} file.')
             print("\n")
             f_d["u"] = info[addr][0]
             datas_t =json.dumps(f_d)
             send(datas_t.encode('utf-8'),conn)
             
    except:
            pass
        

if __name__ == '__main__':
    initialize_client()