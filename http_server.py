import socket


def main():
    port = 80
    if True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        print('Server is up and running')
        try:

            server_socket.listen()
            client_socket, client_address = server_socket.accept()
            print(client_address[0] + " connected")
            serve_client(client_socket, client_address[0])
        except Exception as e:
            print(e)


def serve_client(client_socket, client_address):
    typedict = {
        "jpg": "Content-Type: image/jpeg\r\n",
        "txt": "Content-Type: text/html; charset=utf-8\r\n",
        "html": "Content-Type: text/html; charset=utf-8\r\n",
        "js": "Content-Type: text/javascript; charset=UTF-8\r\n",
        "css": "Content-Type: text/css\r\n"
    }

    while True:
        try:
            data = client_socket.recv(9999).decode()
            print("Client sent:" + data)
            print("-------------")

            if "GET" == data[0:3] and "HTTP" in data.upper():
                req_file = data.split("\r")[0][5:-9]
                version = "HTTP 1.0\r"
                code = "OK 200\r\n"
                end = req_file.split(".")[-1]
                if req_file == "":
                    with open(r"webroot/index.html", "r") as file:
                        site = file.read()
                        ret = (version + code + typedict[end]).encode() + site.encode()
                        print(ret)
                        client_socket.send(ret)
                elif end == "jpg":
                    with open("webroot/" + req_file, "rb") as file:
                        site = file.read()
                        ret = (version + code + typedict[end]).encode() + site.hex().encode()
                        print(ret)
                        client_socket.send(ret)
                else:
                    with open("webroot/" + req_file, "r") as file:
                        site = file.read()
                        ret = (version + code + typedict[end]).encode() + site.encode()
                        print(ret)
                        client_socket.send(ret)
        except Exception as e:
            print(e)
            print("connection terminated")


'''def assemble_response():
    response = f"""HTTP/1.1 200 OK\r\n
    Date: {}\r\n
    Server {}
    """'''


if __name__ == "__main__":
    main()

