import socket
import threading
from auth import authenticate
from crypto import generate_key, encrypt_message, decrypt_message

# Dicionários para mapear usuários, sockets e chaves
clients_by_username = {}
clients_by_socket = {}
keys_by_username = {}

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

        # Gerar e enviar chave AES para o cliente
        key = generate_key()
        keys_by_username[username] = key
        client_socket.send(key)

        # Registrar cliente
        print(f"Nova conexão autenticada: {username}")
        clients_by_username[username] = client_socket
        clients_by_socket[client_socket] = username

        while True:
            encrypted_data = client_socket.recv(1024).decode('utf-8')
            data = decrypt_message(key, encrypted_data)

            # Tratamento de mensagem
            if data == "SAIR":
                break
            recipient, message = data.split(":", 1)
            broadcast(message, recipient, username)
    except Exception as e:
        print(f"Erro com cliente {clients_by_socket.get(client_socket, 'desconhecido')}: {e}")
    finally:
        remove_client(client_socket)

# Enviar mensagem criptografada para um cliente específico
def broadcast(message, recipient, sender):
    if recipient in clients_by_username:
        recipient_socket = clients_by_username[recipient]
        recipient_key = keys_by_username[recipient]
        encrypted_message = encrypt_message(recipient_key, f"{sender}: {message}")
        recipient_socket.send(encrypted_message.encode('utf-8'))
    else:
        print(f"Usuário {recipient} não encontrado.")

def remove_client(client_socket):
    username = clients_by_socket.get(client_socket)
    if username:
        del clients_by_username[username]
        del keys_by_username[username]
    if client_socket in clients_by_socket:
        del clients_by_socket[client_socket]
    client_socket.close()

# Configuração do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Servidor aguardando conexões...")

while True:
    client_socket, address = server_socket.accept()
    print(f"Conexão recebida de {address}")
    threading.Thread(target=handle_client, args=(client_socket,)).start()
