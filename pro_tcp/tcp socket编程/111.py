import socketserver

class Myserver(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        print(self.client_address)
        conn.sendall("我能同时处理多个请求！")
        flag = True
        while flag:
            data = conn.recv(1024)
            if data == "exit":
                flag = False
            else:
                conn.sendall(data)

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("localhost",8000),Myserver)
    server.serve_forever()