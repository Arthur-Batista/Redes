import socket
import threading

list_clients = {}

def handle_client(client_socket, username):
    print(f"Nova conexão: {username}")
    list_clients [username] = client_socket
    list_clients [client_socket] = username

    while True:
        try:
            sending = list_clients[client_socket]
            usersendr = client_socket.recv(1024).decode('utf-8')
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Mensagem recebida de {sending}: {message}")
            broadcast(message, usersendr, sending)
        except:
            print(f"Cliente {sending} desconectado.")
            del list_clients[sending]
            break

def broadcast(message, sender_socket, sending):

    client = list_clients[sender_socket]
    message = (f'{sending}: {message}')
    client.send(message.encode('utf-8'))
    print(f'Mensagem enviada para:{sender_socket}')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Servidor aguardando conexões...")

while True:
    client_socket, address = server_socket.accept()
    username = client_socket.recv(1024).decode('utf-8')
    threading.Thread(target=handle_client, args=(client_socket, username)).start()