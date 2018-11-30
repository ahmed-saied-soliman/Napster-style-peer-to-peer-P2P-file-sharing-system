import rpyc
import pickle
from rpyc.utils.server import ThreadedServer
from constRPYC import *

class server(rpyc.Service):
    peers={}

    def exposed_Register(self,port,file):
        for x in file:
            if(port in self.peers):
                self.peers[port].append(x)
            else:
                self.peers[port]=[x]
        return self.peers

    def exposed_Peers(self):
        return self.peers

    def exposed_Search(self,file):
        PORTS=[]
        for port in self.peers:
            for nameoffile in self.peers[port]:
                arr1=nameoffile.split("/")
                arr1=arr1[len(arr1)-1]
                if file==arr1:
                    PORTS.append(port)
        return PORTS

    def exposed_FilePath(self,port,file):
        for nameoffile in self.peers[port]:
            arr1 = nameoffile.split("/")
            arr1 = arr1[len(arr1) - 1]
            if arr1==file:
                return nameoffile
    def exposed_Terminate(self,port):
        if (port in self.peers):
            del self.peers[port]
        else:
            quit()

if __name__ == "__main__":
    server = ThreadedServer(server, hostname=SERVER, port=PORT)
    server.start()


