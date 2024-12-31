import socket
import threading

# Dicionários para mapear usuários e sockets
clients_by_username = {}
clients_by_socket = {}

# Função para lidar com cada cliente
def handle_client(client_socket):
    try:
        # Receber o nome de usuário
        username = client_socket.recv(1024).decode('utf-8')
        if not username:
            print("Conexão recusada: nome de usuário inválido.")
            client_socket.close()
            return
        
        # Registrar cliente
        print(f"Nova conexão: {username}")
        clients_by_username[username] = client_socket
        clients_by_socket[client_socket] = username
        
        #Recebendo usuário de destino
        usersendr = client_socket.recv(1024).decode('utf-8')
        # Loop para receber mensagens
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == "SAIR":
                usersendr = client_socket.recv(1024).decode('utf-8')
                continue
            
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
