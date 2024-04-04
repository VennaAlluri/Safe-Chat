from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label
from tkinter import *
from tkinter import *
from socket import *
import _thread
from socket import *
import _thread
from AES import *
import json
import RSA
from tkinter import filedialog
import base64
import secrets
import string
import sys

def initialize_client():
    global idn, se_k
    # initialize socket
    s = socket(AF_INET, SOCK_STREAM)
    # config details of the server
    user = sys.argv[2]  # Access e_1 from gu.py
    host = sys.argv[1]  # Access e_2 from gu.py
    port = 1234
    public_key, private_key = RSA.generate_keypair()
    data_to_send = {'user': user, 'rsa':public_key}

# Convert the data to a JSON string
    json_data = json.dumps(data_to_send)
    # connect to server
    s.connect((host, port))
    s.send(json_data.encode('utf-8'))
    dn = s.recv(10240).decode('utf-8')
    d_s = json.loads(dn)
    idn = d_s['pub']
    se_k = RSA.RSA_decrypt(d_s['key'],private_key)
    s_info = d_s['s_info']
    kl = d_s['info']
    print(kl)
    ko = f'{s_info}'
    fp = "Connection established Successfully.\n"
    for i in kl.split(','):
      if len(i)!=0: 
       update_user(i)
    update_chat(fp,1)
    update_chat(ko,1)
    return s
def update_chat(msg,s):
    chatlog.config(state=NORMAL)
    # update the message in the window
    if s == 1:
     chatlog.insert(END, f'{msg}\n')
    if s==2 :
       chatlog.insert(END, f'{msg}')
    if s==0:
     chatlog.insert(END, f'YOU :{msg}')
    chatlog.config(state=DISABLED)
    # show the latest messages
    chatlog.yview(END)
def update_user(m):
    label1.config(state=NORMAL)

    label1.insert(END, f'{m}\n')
    label1.config(state=DISABLED)
    # show the latest messages
    label1.yview(END)

def send():
    key = ''.join(secrets.choice(string.ascii_letters) for _ in range(16))
    j = RSA.RSA_encrypt(key,idn)  
    msg = entry_1.get("0.0", END)
    update_chat(msg,0)
    msg = encrypt(msg,key)
    data_to_send = {'data': msg, 'rsa':j,'op':0}
# Convert the data to a JSON string
    json_data = json.dumps(data_to_send)
    s.send(json_data.encode('utf-8'))
    entry_1.delete("0.0", END)

def send_f():
        j1 = "Sending the file.\n"
        update_chat(j1,1)
        filename = filedialog.askopenfilename()
        ext = filename.split(".")[-1]
        with open(filename, 'rb') as image_file:
          image_binary = image_file.read()
        image_base64 = base64.b64encode(image_binary)
        with open('encoding.txt', 'wb') as text_file:
          text_file.write(image_base64)

        with open('encoding.txt', 'r') as text_file:
           image_base64 = text_file.read()
        
        g = encrypt(image_base64,se_k)
        g = g.encode('utf-8')
# Store the encrypted data as a string in a text file
        with open('encoding.txt', 'wb') as text_file:
          text_file.write(g)


        # Open the text file to send
        with open('encoding.txt', 'rb') as file:
            file_data = file.read()
        data_to_send = {'ext': ext, 'file_data': base64.b64encode(file_data).decode('utf-8'),'op':1}

# Convert the data to a JSON string
        json_data = json.dumps(data_to_send)
        # Send the file data to the server
        s.sendall(json_data.encode('utf-8'))
        

        jo = "File sent successfully.\n"
        update_chat(jo,1)
def receive():
       while 1:
         try:
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
            if f_d["op"]==1:
             ext = f_d["ext"]
             print(ext)
             file_data = f_d['file_data']
             with open('decoding.txt', 'wb') as file:
              file.write(base64.b64decode(file_data.encode('utf-8')))

             add = f'receivedfile.{ext}'
             with open('decoding.txt', 'rb') as text_file:
                 image_base64 = text_file.read()

             image_base64 = image_base64.decode('utf-8')
             dec = decrypt(image_base64, se_k)
             decoded_image_binary = base64.b64decode(dec)

             with open(add, 'wb') as output_image:
                output_image.write(decoded_image_binary)

             mi = f'{ext} file received successfully from {f_d["u"]}.\n'
             update_chat(mi,1)
            if f_d["op"]==3:
               pl = f'{f_d["name"]} connected to the chat.\n'
               update_chat(pl,1)
               update_user(f_d['name'])
            else:
               ml = f'{f_d["u"]} :{f_d["data"]}'
               update_chat(ml,2)
             
         except:    
              pass

# update the chat log
def press(event):
    send()
def GUI():
    global entry_1,chatlog,s,label1
    window = Tk()
    width = window.winfo_screenwidth() 
    height = window.winfo_screenheight()
    window.geometry(f"{width}x{height}")
    window.configure(bg = "#2C2C2C")
    scale_x = 1536/width
    scale_y = 864/height
    canvas = Canvas(
        window,
        bg = "#2C2C2C",
        height = height,
        width = width,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.pack()


    button_image_1 = PhotoImage(file="button_1.png")
    button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,
        command=lambda: send_f()
    )
    button_1.place(x=1395.0,y=760.0,width=59.0,height=56.0)

    button_image_2 = PhotoImage(file="button_2.png")
    button_2 = Button(image=button_image_2,borderwidth=0,highlightthickness=0,
        command=lambda: send()
    )
    button_2.place(x=1455.0,y=760.0,width=59.0,height=56.0)

    canvas.create_rectangle(
        457.0,
        765.0,
        1380.0,
        810.0,
        fill="#1E1E1E",
        outline="#0966ff",
        width=2.7)
 
    entry_1 =Text(bd=0,bg="#1E1E1E",fg="#000716",highlightthickness=0)
    entry_1.configure(font=("RobotoRoman ExtraBold", 21),fg="#FFFFFF")
    entry_1.place(x=457.0,y=765.0,width=923.0,height=45.0)



    canvas.create_rectangle(
        441.0,
        17.0,
        1515.0,
        718.0,
        fill="#1E1E1E",
        outline="#0966ff",
        width=2.7)
    canvas.create_rectangle(
        13.0,
        17.0,
        425.0,
        818.0,
        fill="#1E1E1E",
        outline="#0966ff",
        width=2.7)



    lx1, ly1, lw1, lh1 = 13.0, 17.0, 412.0, 800.0
    label1 = Text(bg="#1E1E1E",bd=2.5)
    label1.config(state="disabled")
    label1.configure(font=("RobotoRoman ExtraBold", 21),fg="#FFFFFF")
    label1.place(x=lx1,y=ly1,width=lw1,height=lh1)

    lx2, ly2, lw2, lh2 = 442.0, 17.0, 1072.0, 700.0
    chatlog = Text(bg="#1E1E1E",bd=2.5)
    chatlog.config(state="disabled")
    chatlog.configure(font=("RobotoRoman ExtraBold", 21),fg="#FFFFFF")
    chatlog.place(x=lx2,y=ly2,width=lw2,height=lh2)
    s = initialize_client()
    _thread.start_new_thread(receive, ())
    entry_1.bind("<KeyRelease-Return>", press)

    window.mainloop()

if __name__ == '__main__':
    chatlog = textbox = None
    GUI()