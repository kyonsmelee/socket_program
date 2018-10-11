import asyncore, socket

HOST = '192.168.100.70'
PORT = 8000
BufSize = 1024
NoOfClients = 5

class SockHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(BufSize)
        print 'data:',data
        if data:
            self.send(data)

class SockServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((HOST,PORT))
        self.listen(NoOfClients)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr[0]))
            handler = SockHandler(sock)

server = SockServer(HOST,PORT)
print 'wait...'
asyncore.loop()
