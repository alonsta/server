import socket
import threading
import protocols
import server_procs


def main():
    port = 7002
    '''if server_procs.sus(port):
        return'''
    if True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        print('Server is up and running')
        try:
            while True:
                server_socket.listen()
                client_socket, client_address = server_socket.accept()
                print(client_address[0] + " connected")
                msg = "welcome to my server. what would you like to do(h?)"
                protocols.log_requests(protocols.log_format("connected", client_address[0], msg))
                client_socket.send(protocols.format_z(msg).encode(errors="replace"))
                th1 = threading.Thread(target=serve_client, args=(client_socket, client_address[0]))
                th1.start()
        except Exception as e:
            msg = protocols.log_format("except", "000.000.000.000", e)
        server_procs.close_port(port)


def serve_client(client_socket, client_address):
    while True:
        byt = client_socket.recv(4).decode(errors="replace")
        byt2 = client_socket.recv(int(byt)).decode(errors="replace")
        data = client_socket.recv(int(byt2)).decode(errors="replace").lower()
        print(client_address + " sent: " + str(data))

        if data == "exit":
            msg = "Connection terminated by client."
            client_socket.send(protocols.format_z(msg).encode(errors="replace"))
            break

        msg = server_procs.answer(data)
        client_socket.send(protocols.format_z(msg).encode(errors="replace"))
        protocols.log_requests(protocols.log_format(data, client_address, msg))
    client_socket.close()


if __name__ == "__main__":
    main()