import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {IP}:{PORT}')

def receive_voice_note(client_socket):
    try:
        voice_note_header = client_socket.recv(HEADER_LENGTH)

        if not len(voice_note_header):
            return False

        voice_note_length = int(voice_note_header[:HEADER_LENGTH])

        return {'header': voice_note_header[:HEADER_LENGTH], 'data': client_socket.recv(voice_note_length)}    

    except:
        # Something went wrong like empty voice_note or client exits abruptly
        return False    

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_voice_note(client_socket)
            if user == False:
                continue
            
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('')
        
        else:
            voice_note = receive_voice_note(notified_socket)

            if voice_note == False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue

            # Iterate over connected clients and broadcast voice_note
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:

                    # Send user and voice_note (both with their headers)
                    # We are reusing here voice_note header sent by sender, and saved username header send by user when he connected
                    client_socket.send(user['header'] + user['data'] + voice_note['header'] + voice_note['data'])

    # Not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]