import FileSys
from tkinter import *
from interface import *
#from server import *


if __name__ == '__main__':

    app = interface().create()
    '''direct_1 = FileSys.Directory("Documente")
    file_1 = FileSys.File("Fis_1", "asta e fis_1")
    file_2 = FileSys.File("Fis_2", "asta e fis_2")

    direct_1.add_child(file_1)
    direct_1.add_child(file_2)

    print(direct_1)'''


    app.mainloop()




