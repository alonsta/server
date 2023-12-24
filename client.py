import codecs
import socket
import protocols


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\

client_socket.connect(('127.0.0.1', 7002))

byt = client_socket.recv(4).decode(errors="replace")
byt2 = client_socket.recv(int(byt)).decode(errors="replace")
data = client_socket.recv(int(byt2)).decode(errors="replace")
print("server sent: " + data)
while True:
    data_to_send = input("Your request:  ")
    client_socket.send(protocols.format_z(data_to_send).encode(errors="replace"))

    byt = client_socket.recv(4).decode(errors="replace")
    byt2 = client_socket.recv(int(byt)).decode(errors="replace")
    data_r = client_socket.recv(int(byt2))
    data = data_r.decode(errors="replace")
    print("server sent: " + data)
    if len(data) > 50000:
        ans = input("save this screenshot? if so. write the place to decode it into(path). else say 'no': ")
        if ans == "no":
            continue
        try:
            data = codecs.decode(data_r)
            with open(ans, "wb") as image:
                image.write(bytes.fromhex(data))

        except Exception as e:
            print(f"an {e} occurred")