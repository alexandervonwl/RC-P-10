from tkinter import *


class interface():
    def create(self):
        root = Tk()

        root.title("Server CoAP")
        root.geometry("500x800") #You want the size of the app to be 500x800
        root.resizable(0,0) #Don't allow resizing in the x or y direction

        #cele 2 frameuri, 1 pentru loguri si unul pentru mesaje
        frameLogged = Frame(root, borderwidth=5, bg="black")
        frameReceived = Frame(root, borderwidth=5, bg="black")
        frameLogged.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        frameReceived.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #frameLogged.pack(fill=tk.BOTH, expand=1)  # Expand the frame to fill the root window

        #labeluri introduse in frameurile mai sus mentionate
        labelLogged = Label(frameLogged, text='Conexiuni:', bg="black", fg="white")
        labelReceived = Label(frameReceived, text='Mesaje:', bg="black", fg="white")

        labelLogged.grid(row=0, column=0)
        labelReceived.grid(row=0, column=0)

        frameLogged.grid(row=0, column=0, sticky="nsew")
        frameReceived.grid(row=1, column=0, sticky="nsew")

        root.grid_rowconfigure(0, weight=1, uniform="group1")
        root.grid_rowconfigure(1, weight=3, uniform="group1")
        root.grid_columnconfigure(0, weight=1)

        return root
        #O punem pe ecran
        #myLabel.pack()



