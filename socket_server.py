from socket import socket, AF_INET, SOCK_STREAM
import os, sys, threading

server_addr = ''
server_port = 50005


# SERVER
################################################################################
def server():
    """
        Description
        ----
        Created to verify computer-to-computer communications
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((server_addr, server_port))
    sock.listen(3)

    print("Server started")

    while True:
        conn, addr = sock.accept()  # Wait for next client to connect
        #conn.timeout(5)
        print("Server connected by", addr)
        conn.send(b"Hello from MBP")
        conn.close()

# CLIENT
################################################################################
def client():
    """
        Description
        ----

    """
    hostname = "localhost"

    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((hostname, server_port))

    while True:
        data = sockobj.recv(1024)
        if (data):
            print("Client reveived:", data)
            break

    sockobj.close()

#==============================================================================#
if __name__ == "__main__":
    if len(sys.argv) == 1:
        server()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "client":
            client()
        elif sys.argv[1] == "server":
            server()
        elif sys.argv[1] == "both":
            client_thrd = threading.Thread(target=client)
            client_thrd.start()
            server()
            client_thrd.join()
    else:
        raise SyntaxError("Usage: socket_server both")


