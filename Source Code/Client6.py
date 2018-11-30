import rpyc
import pickle
from constRPYC import *
from threading import Thread
from rpyc.utils.server import ThreadedServer

class Client6(rpyc.Service):
    def exposed_UploadFile(self,file):
        lines = []
        file = open(file, 'rb')
        for line in file:
            lines.append(line)
        file.close()
        data=pickle.dumps(lines)
        return data

    def exposed_DownloadFile(self,files,data):
        newdata=pickle.loads(data)
        file = open(files, 'wb')
        for line in newdata :
            file.write(line)
        file.close()



if __name__ == "__main__":
    client6 = ThreadedServer(Client6, hostname=SERVER, port=PORT6)
    client_server_thread = Thread(target=client6.start)
    client_server_thread.daemon = True
    client_server_thread.start()
    Files=[]
    menu = {}
    menu['1'] = "Register"
    menu['2'] = "Search & Download File"
    menu['3'] = "Terminate"
    conn = rpyc.connect(SERVER,PORT)
    while True:
        options = menu.keys()
        options.sort()
        for entry in options:
            print entry, menu[entry]

        selection = raw_input("Please Select :")
        if selection == '1':
            Fileslen=input("How Many Files ? ")
            while len(Files)<Fileslen:
                File = raw_input("Enter your File to the List : ")
                Files.append(File)
            print(conn.root.exposed_Register(PORT6,Files))
            Files=[]
        elif selection == '2':
            print(conn.root.exposed_Peers())
            NameOfFile=raw_input("Enrer File Name to Search About & Download It : ")
            print(conn.root.exposed_Search(NameOfFile))
            listofports=conn.root.exposed_Search(NameOfFile)
            ch = input("Choose One Of These PORTS : ")
            if ch in listofports:
                FilePath = conn.root.exposed_FilePath(ch, NameOfFile)
                conn2 = rpyc.connect(SERVER, ch)
                Lines = conn2.root.exposed_UploadFile(FilePath)
                files = raw_input("Save AS EX:aaa.txt : ")
                conn2.root.exposed_DownloadFile(files, Lines)
            else:
                print("This PORT NOT Found!!")
        elif selection == '3':
            conn.root.exposed_Terminate(PORT6)
            quit()

        else:
            print("SomeThing Wrong!!")