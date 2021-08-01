import socket
from bitarray import bitarray


class Emisor(object):

    def __init__(self):
        self.mensaje = None
        self.mensaje_ruidoso = None
        self.socket = None
        self.localhost_ip = "localhost"
        self.port = 80

    def enviar_cadena(self):
        # Aplicacion
        self.mensaje = input("Escriba el mensaje que desea enviar: ")

    def enviar_cadena_segura(self):
        # Verificacion
        self.mensaje = bitarray(self.mensaje)

    def agregar_ruido(self):
        # Ruido
        self.mensaje_ruidoso = self.mensaje
        print(self.mensaje_ruidoso)
        print(self.mensaje_ruidoso.tobytes())

    def enviar_objeto(self):
        # Transmision
        self.socket = socket.socket()
        self.socket.connect((self.localhost_ip, self.port))
        self.socket.send(self.mensaje_ruidoso)
        self.socket.close()


emisor = Emisor()

while True:
    print("Menu:")
    opcion = int(input("""
    1. Enviar mensaje
    0. Salir
    """))

    if opcion == 0:
        print("Bye")
        exit()
    elif opcion == 1:
        emisor.enviar_cadena()
        emisor.enviar_cadena_segura()
        emisor.agregar_ruido()
        emisor.enviar_objeto()
    else:
        pass
