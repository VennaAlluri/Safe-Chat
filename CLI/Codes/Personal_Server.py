from socket import *
import _thread
from AES import *
import json
import RSA
from tkinter import filedialog
import base64
import secrets
import string

def initialize_client():
    global name,r_s,private_key
    # initialize socket
    s = socket(AF_INET, SOCK_STREAM)
    # config details of server
    Username = input("\nUsername :")
    host = input("Ip Address of your device :")  ## to use between devices in the same network eg.192.168.1.5
    port = 1234
    public_key, private_key = RSA.generate_keypair()
    # initialize server
    s.bind((host, port))
    print("\nServer established Successfully")
    # set no. of clients
    s.listen(1)
    print("Waiting for User to Connect.")
    # accept the connection from client
    conn, addr = s.accept()
    print("User Connected Successfully.\n")
    user_2 = conn.recv(1024).decode('utf-8')
    ds = json.loads(user_2)
    name = ds["user"]
    r_s = ds["rsa"]
    data_to_send = {'name': Username, 'rsa':public_key}

# Convert the data to a JSON string
    json_data = json.dumps(data_to_send)
    conn.send(json_data.encode('utf-8'))
    return conn
    
def send():
    key = ''.join(secrets.choice(string.ascii_letters) for _ in range(16))
    j = RSA.RSA_encrypt(key,r_s)
    while 1 :   
        msg = input()
        if msg == "Send":
            send_f()
        msg = encrypt(msg,key)
        data_to_send = {'data': msg, 'rsa':j,'op':0}
# Convert the data to a JSON string
        json_data = json.dumps(data_to_send)
        s.send(json_data.encode('utf-8'))
        print("msg sent")


def send_f():
        key = ''.join(secrets.choice(string.ascii_letters) for _ in range(16))
        e_k = RSA.RSA_encrypt(key,r_s)
        filename = filedialog.askopenfilename()
        print("Sending.")
        ext = filename.split(".")[-1]
        with open(filename, 'rb') as image_file:
          image_binary = image_file.read()
        image_base64 = base64.b64encode(image_binary)
        with open('Encoding.txt', 'wb') as text_file:
          text_file.write(image_base64)

        with open('Encoding.txt', 'r') as text_file:
           image_base64 = text_file.read()
        
        g = encrypt(image_base64,key)
        g = g.encode('utf-8')
# Store the encrypted data as a string in a text file
        with open('Encoding.txt', 'wb') as text_file:
          text_file.write(g)


        # Open the text file to send
        with open('Encoding.txt', 'rb') as file:
            file_data = file.read()
        data_to_send = {'ext': ext, 'file_data': base64.b64encode(file_data).decode('utf-8'),'op':1,'aes_key':e_k}

# Convert the data to a JSON string
        json_data = json.dumps(data_to_send)
        # Send the file data to the server
        s.sendall(json_data.encode('utf-8'))
        

        print("File sent successfully.")
        send()
def receive():
 while 1:
    try:
            '''data = conn.recv(10240).decode('utf-8')
            ds = json.loads(data)'''
            datas = b""
            o=1
            while o!=0:
              data = s.recv(1024)
              datas += data
              if datas[-1]==125:
                  o=0
                  break
            f_d = datas.decode('utf-8')
            f_d = json.loads(f_d)
            if f_d["op"]==0:
                msg = decrypt(f_d["data"],RSA.RSA_decrypt(f_d["rsa"],private_key))
                print(f'{name} :'+msg)
            else:
             ext = f_d["ext"]
             file_data = f_d['file_data']
             with open('Decoding.txt', 'wb') as file:
              file.write(base64.b64decode(file_data.encode('utf-8')))

             add = f'receivedfile.{ext}'
             with open('Decoding.txt', 'rb') as text_file:
                 image_base64 = text_file.read()

             image_base64 = image_base64.decode('utf-8')
             dec = decrypt(image_base64, RSA.RSA_decrypt(f_d["aes_key"],private_key))
             decoded_image_binary = base64.b64decode(dec)

             with open(add, 'wb') as output_image:
                output_image.write(decoded_image_binary)

             print(f'{ext} File received successfully from {name}.')
             
    except:
            pass

def strt():
    global s
    s = initialize_client()
    _thread.start_new_thread(receive, ())
    send()