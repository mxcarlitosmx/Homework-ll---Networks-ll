import socket
import threading
import sys

def recibir_mensajes(sock):
    #Hilo encargado de recibir datos del servidor.
    while True:
        try:
            mensaje = sock.recv(1024).decode('ascii')
            if mensaje:
                print(f"\n{mensaje}")
                print("> ", end="")
            else:
                break
        except:
            print("Conexion perdida con el servidor.")
            sock.close()
            break

def enviar_mensajes(sock):
    #Hilo principal o secundario para enviar datos.
    while True:
        mensaje = input("> ")
        if mensaje.lower() == 'salir':
            sock.close()
            break
        sock.send(mensaje.encode('ascii'))

#Configuracion Cliente
if len(sys.argv) != 3:
    print("Usa: python cliente.py <host> <puerto>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

nickname = input("Ingresa tu nombre: ")
client.send(nickname.encode('ascii'))

# Iniciar hilo de recepcion
thread_recibir = threading.Thread(target=recibir_mensajes, args=(client,))
thread_recibir.daemon = True # Se cierra si el principal se cierra
thread_recibir.start()

#El hilo principal se queda enviando mensajes
enviar_mensajes(client)
