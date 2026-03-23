import socket
import threading
import sys

# Usaremos un diccionario para mapear: {socket: nickname}
clientes = {}

def broadcast(mensaje, _cliente_socket):
    #Enviar mensaje a todos los clientes excepto al que lo mando
    for sock in clientes:
        if sock != _cliente_socket:
            try:
                sock.send(mensaje)
            except:
                # Si falla el envio, es probable que la conexion esta rota
                remover_cliente(sock)

def remover_cliente(sock):
    if sock in clientes:
        nickname = clientes[sock]
        print(f"Desconectando a {nickname}")
        del clientes[sock]
        sock.close()
        broadcast(f"[Servidor]: {nickname} ha salido del chat.".encode('ascii'), sock)

def recibir_datos(conn, addr):
    try:
        # 1. El primer mensaje que envia el cliente es su nombre
        nickname = conn.recv(1024).decode('ascii')
        clientes[conn] = nickname
        print(f"Cliente conectado: {addr} ({nickname})")
        
        # Notificar a los demás que alguien entró
        broadcast(f"[Servidor]: {nickname} se ha unido al chat".encode('ascii'), conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # Formatear el mensaje: [Nickname]: Mensaje
            mensaje_formateado = f"[{nickname}]: {data.decode('ascii')}".encode('ascii')
            print(f"Enviando: {mensaje_formateado.decode('ascii')}")
            broadcast(mensaje_formateado, conn)
            
    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        remover_cliente(conn)

def servirPorSiempre(socketTcp):
    print("Servidor escuchando...")
    while True:
        client_conn, client_addr = socketTcp.accept()
        # Creamos el hilo para este cliente
        thread = threading.Thread(target=recibir_datos, args=(client_conn, client_addr))
        thread.start()

#Configuracion inicial
if len(sys.argv) != 3:
    print("Usa: python servidor.py <host> <puerto>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((host, port))
    TCPServerSocket.listen()
    servirPorSiempre(TCPServerSocket)
