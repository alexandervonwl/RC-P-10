from tkinter import *
from server import Server
import threading


class interface():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = Server()

    def on_connect(self):
        self.server_thread = threading.Thread(target=lambda: self.start_server()).start()

    def start_server(self):
        self.server.run()

    def stop_server(self):
        self.server.is_running = FALSE

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
        labelTitluLogged = Label(frameLogged, text='Conexiuni:', bg="black", fg="white")
        labelTitluReceived = Label(frameReceived, text='Mesaje:', bg="black", fg="white")
        labelConnection = Label(frameLogged, text = self.server.label, bg="black", fg="white")

        startButton = Button(frameLogged, text='Start Server', bg="green", command=self.on_connect)
        stopButton = Button(frameLogged, text='Stop Server', bg="red", command=self.stop_server)

        labelTitluLogged.grid(row=1, column=0)
        labelTitluReceived.grid(row=0, column=0)
        labelConnection.grid(row=2, column=0)
        startButton.grid(row=0, column="0")
        stopButton.grid(row=0, column=1)

        frameLogged.grid(row=0, column=0, sticky="nsew")
        frameReceived.grid(row=1, column=0, sticky="nsew")

        root.grid_rowconfigure(0, weight=1, uniform="group1")
        root.grid_rowconfigure(1, weight=3, uniform="group1")
        root.grid_columnconfigure(0, weight=1)

        print(self.server.label)
        return root
        #O punem pe ecran
        #myLabel.pack()



