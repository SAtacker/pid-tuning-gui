import socket 
import sys
import json
from multiprocessing import Process
from multiprocessing import Queue

class tcp_server():
    def __init__(self, port=1212):
        self.message_pipe = Queue()
        self.proc = None

        self.port = port
        self.family_addr = socket.AF_INET
        self.conn = None
        self.addr = None
        
        try: 
            self.sock = socket.socket(self.family_addr, socket.SOCK_STREAM)
        
        except socket.error as msg:
            print(f'failed to create socket. error code: {str(msg[0])} Message {msg[1]}')
    
    def recv_data(self, size):
        return_dict = {
            "data" : None,
            "error" : None
        }
        
        try:
            data = self.conn.recv(size)
            
            if data:
                return_dict["data"] = data

        except socket.error as msg:
            return_dict["error"] = msg

        return return_dict

    def send_data(self, data):
        try:
            self.conn.sendall(data.encode())
        
        except socket.error as msg:
            return msg
        
        return None

    def shutdown(self):
        self.sock.close()

    def handler(self, control_var=True):
        try:
            self.sock.bind(('', self.port))
            print('socket binded')
            self.sock.listen(1)
            print('socket listening')
            self.conn, self.addr = self.sock.accept()
            print('connected by', self.addr)

        except socket.error as msg:
            print('Error: ' + str(msg[0]) + ': ' + msg[1])
            self.sock.close()
            sys.exit(1)
        
        while control_var:
            data = self.message_pipe.get()
            data_len = len(data)
            recv_len = -10
            
            while recv_len != data_len:
                self.send_data(data)
                recv_dict = self.recv_data(15)

                if recv_dict["error"] is None:
                    recv_len = int(recv_dict["data"].decode())

            print('message sent successfully')

        self.proc.join()

    def run(self, control_var):
        self.proc = Process(target=self.handler, kwargs={'control_var':control_var})
        self.proc.start()
