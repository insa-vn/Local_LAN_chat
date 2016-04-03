from threading import Thread
import socket
import select

# network constants
HOST = 'localhost'
PORT = 5000
RECV_BUFFER = 4096

# global variables
server_socket = ''
accepted_socket = ''
socket_list = []

# ---------------------------------------------------#
# ---------INITIALIZE CONNECTION VARIABLES-----------#
# ---------------------------------------------------#


def init_connection():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    socket_list.append(server_socket)


# ---------------------------------------------------#
# ----------------CONNECTION MANAGEMENT--------------#
# ---------------------------------------------------#

# broadcast messages to all connected clients
def broadcast(sender_socket, message):
    global socket_list, server_socket
    for a_socket in socket_list:
        # send the message only to peer
        if (a_socket != server_socket) and (a_socket != sender_socket):
            try:
                a_socket.send(message)
            except socket.error:
                a_socket.close()
                if a_socket in socket_list:
                    socket_list.remove(a_socket)


# run server, messages from clients will be broadcasted
def run_server():

    global accepted_socket, server_socket
    server_socket.listen(10)
    accepted_socket, address = server_socket.accept()
    socket_list.append(accepted_socket)

    while True:

        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)

        for sock_ready2read in ready_to_read:

            # a new connection request received
            if sock_ready2read == server_socket:
                accepted_socket, address = server_socket.accept()
                socket_list.append(accepted_socket)
                broadcast_msg = "%s entered our chatting room\n" % str(address)
                broadcast(accepted_socket, broadcast_msg)

            # a message from a client, not a new connection
            else:
                try:
                    # receiving data from the socket.
                    data = sock_ready2read.recv(RECV_BUFFER)
                    broadcast_msg = "\r" + str(sock_ready2read.getpeername()) + ': ' + data
                    broadcast(sock_ready2read, broadcast_msg)
                except socket.error:
                    # recv method cannot be done means a socket is broken, so it has to be removed
                    sock_ready2read.close()
                    if sock_ready2read in socket_list:
                        socket_list.remove(sock_ready2read)
                    broadcast_msg = "Client %s is offline\n" % str(address)
                    broadcast(server_socket, broadcast_msg)
                    continue

    accepted_socket.close()


if __name__ == '__main__':

    init_connection()
    Thread(target=run_server, name='Server').start()
