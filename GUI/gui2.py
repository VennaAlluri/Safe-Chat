from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Label,messagebox
import subprocess
import os
import socket


def transistion(): 
    global e_1,e_2 
    e_1 = entry_1.get()
    e_2 = entry_2.get()  
    file_to_run = r"Grp_Server_gui.py"
    if e_2 == socket.gethostbyname(socket.gethostname()) and e_1.isdigit():
       window.withdraw()
       subprocess.run(["python", file_to_run,e_1,e_2], check=True)
    if not(e_1.isdigit()):
         message = "Expected Integer value for No of people."
         messagebox.showerror("Error", message)
    else:  
         message = "Invalid Server ID Address, Enter your system IP Address"
         messagebox.showerror("Error", message)
def transistion_1(): 
    window.withdraw()
    file_to_run = r"gui1.py"
    try:
        subprocess.run(["python", file_to_run], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}") 



def GUI():
    global window,entry_1,entry_2
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
    button_image_1 = PhotoImage(file="picture3.png")
    button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=lambda: transistion_1() ,relief="flat")
    button_1.place(x=scale_x*511.0,y=scale_y*685.0,width=470.0,height=65.0)
    button_image_2 = PhotoImage(file="picture2.png")
    button_2 = Button(image=button_image_2,borderwidth=0,highlightthickness=0,command=lambda: transistion() ,relief="flat")
    button_2.place(x=scale_x*511.0,y=scale_y*585.0,width=470.0,height=65.0)
    entry_image_1 = PhotoImage(file="en_1.png")
    entry_bg_1 = canvas.create_image(scale_x*750.0,scale_y*521.5,image=entry_image_1)
    entry_1 = Entry(bd=0,bg="#303134",fg="#000716",highlightthickness=0)
    entry_1.place(x=scale_x*515.0,y=scale_y*494.0,width=466.0,height=53.0)
    entry_1.configure(font=("RobotoRoman ExtraBold", 25),fg="#FFFFFF")
    canvas.create_text(scale_x*520.0,scale_y*455.0,anchor="nw",text="No of People",fill="#FFFFFF",font=("RobotoRoman ExtraBold", 25 * -1))

    entry_image_2 = PhotoImage(file="en_2.png")
    entry_bg_2 = canvas.create_image(scale_x*750.0,scale_y*393.5,image=entry_image_2)
    entry_2 = Entry(bd=0,bg="#303134",fg="#000716",highlightthickness=0)
    entry_2.place(x=scale_x*515.0,y=scale_y*366.0,width=466.0,height=53.0)
    entry_2.configure(font=("RobotoRoman ExtraBold", 25),fg="#FFFFFF")
    canvas.create_text(scale_x*520.0,scale_y*319.0,anchor="nw",text="Server ID",fill="#FFFFFF",font=("RobotoRoman ExtraBold", 25 * -1))

    image_image_1 = PhotoImage(file="image_1.png")
    image_1 = canvas.create_image(scale_x*750.0,scale_y*196.0,image=image_image_1)
    
    window.mainloop()
if __name__ == '__main__':
    GUI()