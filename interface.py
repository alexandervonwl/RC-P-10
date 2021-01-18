from tkinter import *
import tkinter as tk
from server2 import Server
import threading
from queue import Queue



class interface:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = Tk()
        self.root.title("Server CoAP")
        self.root.geometry("500x800")  # You want the size of the app to be 500x800
        self.root.resizable(0, 0)  # Don't allow resizing in the x or y direction
        # cele 2 frameuri, 1 pentru loguri si unul pentru mesaje
        self.frameLogged = Frame(self.root, borderwidth=5, bg="black")
        self.frameReceived = Frame(self.root, borderwidth=5, bg="black")
        self.frameLogged.pack_propagate(0)  # Don't allow the widgets inside to determine the frame's width / height
        self.frameReceived.pack_propagate(0)  # Don't allow the widgets inside to determine the frame's width / height
        # frameLogged.pack(fill=tk.BOTH, expand=1)  # Expand the frame to fill the root window

        # cream butoanele/labelurile pe care le introducem in frameurile mai sus mentionate
        self.labelTitluLogged = Label(self.frameLogged, text='Conexiuni:', bg="black", fg="white")
        self.labelTitluReceived = Label(self.frameReceived, text='Mesaje:', bg="black", fg="white")
        self.labelConnection = Label(self.frameLogged, text="", bg="black", fg="white")
        self.labelMesaj = []
        self.indexMesaj = 0
        self.labelMesaj.append(Label(self.frameReceived, text="", bg="black", fg="white"))
        self.labelMesaj.append(Label(self.frameReceived, text="", bg="black", fg="white"))
        self.labelMesaj.append(Label(self.frameReceived, text="", bg="black", fg="white"))
        #self.labelMesaj1 = Label(self.frameReceived, text="", bg="black", fg="white")
        #self.labelMesaj2 = Label(self.frameReceived, text="", bg="black", fg="white")

        # cream butoanele pe care le introducem in frameul Logged
        self.startButton = Button(self.frameLogged, text='Start Server', bg="green", command=self.on_connect)
        self.stopButton = Button(self.frameLogged, text='Stop Server', bg="red", command=self.stop_server)

        # adaugam label/butoane la frame
        self.labelTitluLogged.grid(row=1, column=0)
        self.labelTitluReceived.grid(row=0, column=0)
        self.labelConnection.grid(row=2, column=0)
        for i in range(len(self.labelMesaj)):
            self.labelMesaj[i].grid(row=i+2, column=0)
        self.startButton.grid(row=0, column="0")
        self.stopButton.grid(row=0, column=1)

        self.frameLogged.grid(row=0, column=0, sticky="nsew")
        self.frameReceived.grid(row=1, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1, uniform="group1")
        self.root.grid_rowconfigure(1, weight=3, uniform="group1")
        self.root.grid_columnconfigure(0, weight=1)


        self.server = Server(self)

    def on_connect(self):
        self.server_thread = threading.Thread(target=lambda: self.start_server()).start()

    def start_server(self):
        self.connection = self.server.run()

    def stop_server(self):
        self.server.is_running = FALSE

    def create(self):
        return self.root

        # O punem pe ecran
        # myLabel.pack()