import socket
import threading
from auth import authenticate

# Dicionários para mapear usuários e sockets
clients_by_username = {}
clients_by_socket = {}

# Lista de usuários e senhas
user_credentials = {
    "usuario1": "senha1",
    "usuario2": "senha2",
    "admin": "admin123"
}

# Função para lidar com cada cliente
def handle_client(client_socket):
    try:
        # Etapa de autenticação
        credentials = client_socket.recv(1024).decode('utf-8')
        is_authenticated, username = authenticate(credentials, user_credentials)

        if not is_authenticated:
            client_socket.send("FALHA".encode('utf-8'))
            client_socket.close()
            return

        client_socket.send("SUCESSO".encode('utf-8'))

        # Registrar cliente
        print(f"Nova conexão autenticada: {username}")
        clients_by_username[username] = client_socket
        clients_by_socket[client_socket] = username

        # Recebendo usuário de destino
        while True:
            usersendr = client_socket.recv(1024).decode('utf-8')

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message == "SAIR":
                    break

                print(f"Mensagem recebida de {username}: {message}")

                # Redirecionar mensagem
                broadcast(message, usersendr, username)
    except Exception as e:
        print(f"Erro com cliente {clients_by_socket.get(client_socket, 'desconhecido')}: {e}")
        remove_client(client_socket)

# Função para enviar mensagem para um cliente específico
def broadcast(message, recipient, sender):
    try:
        if recipient in clients_by_username:
            recipient_socket = clients_by_username[recipient]
            full_message = f"{sender}: {message}"
            recipient_socket.send(full_message.encode('utf-8'))
            print(f"Mensagem enviada para {recipient}: {message}")
        else:
            print(f"Usuário {recipient} não encontrado.")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {recipient}: {e}")

# Função para remover cliente das listas
def remove_client(client_socket, username=None):
    if not username:
        username = clients_by_socket.get(client_socket)
    if username in clients_by_username:
        del clients_by_username[username]
    if client_socket in clients_by_socket:
        del clients_by_socket[client_socket]
    client_socket.close()

# Configuração do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Servidor aguardando conexões...")

# Loop para aceitar conexões
while True:
    client_socket, address = server_socket.accept()
    print(f"Conexão recebida de {address}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
