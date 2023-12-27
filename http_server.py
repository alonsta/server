import socket


def main():
    port = 80
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    print('Server is up and running')
    while True:
        try:
            server_socket.listen()
            client_socket, client_address = server_socket.accept()
            print(client_address[0] + " connected")
            serve_client(client_socket, client_address[0])
        except Exception as e:
            print(e)


def serve_client(client_socket, client_address):
    typedict = {
        "": "",
        "jpg": "Content-Type: image/jpeg\r\n",
        "txt": "Content-Type: text/html; charset=utf-8\r\n",
        "html": "Content-Type: text/html; charset=utf-8\r\n",
        "js": "Content-Type: text/javascript; charset=UTF-8\r\n",
        "css": "Content-Type: text/css\r\n"
    }
    try:
        data = client_socket.recv(2000).decode()
        print("Client sent:" + data)
        print("-------------")

        if "GET" == data[0:3] and "HTTP" in data.upper():
            req_file = data.split("\r\n")[0].split(" ")[1]
            version = "HTTP/1.0\r\n"
            code = "200 OK\r\n"
            end = req_file.split(".")[-1]

            if req_file == "/":
                req_file = "/index.html"

            with open("webroot" + req_file, "rb") as file:
                site = file.read()
                content_type_header = typedict.get(end, "")
                content_length_header = f"Content-Length: {len(site)}\r\n"
                response = (version + code + content_type_header + content_length_header + "\r\n").encode() + site
                client_socket.send(response)

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
