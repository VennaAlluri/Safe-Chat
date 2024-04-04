from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Label
import subprocess


def transistion(): 
    window.withdraw()
    file_to_run = r"gui3.py"
    try:
        subprocess.run(["python", file_to_run], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")  

def transistion_1():
    window.withdraw()
    file_to_run = r"gui2.py"
    try:
        subprocess.run(["python", file_to_run], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}") 


def GUI():
    global window
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
    button_image_2 = PhotoImage(file="picture1.png")
    button_2 = Button(image=button_image_2,borderwidth=0,highlightthickness=0,command=lambda: transistion_1() ,relief="flat")
    button_2.place(x=scale_x*511.0,y=scale_y*400.0,width=470.0,height=65.0)

    button_image_1 = PhotoImage(file="connect.png")
    button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=lambda: transistion() ,relief="flat")
    button_1.place(x=scale_x*511.0,y=scale_y*500.0,width=470.0,height=65.0)
    canvas.create_text(scale_x*550.0,scale_y*300.0,anchor="nw",text="Welcome to the Safe chat.",fill="#FFFFFF",font=("RobotoRoman ExtraBold", 35 * -1))

    

    image_image_1 = PhotoImage(file="image_1.png")
    image_1 = canvas.create_image(scale_x*750.0,scale_y*196.0,image=image_image_1)
    
    window.mainloop()
if __name__ == '__main__':
    GUI()