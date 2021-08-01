import socket
import random
from bitarray import bitarray


class Emisor(object):

    def __init__(self):
        self.socket = None
        self.localhost_ip = "localhost"
        self.port = 80
        self.probabilidad = 1
        self.mensaje = None
        self.mensaje_binario = None
        self.mensaje_ruidoso = None

    def enviar_cadena(self):
        # Aplicacion
        self.mensaje = input("Escriba el mensaje que desea enviar: ")

    def enviar_cadena_segura(self):
        # Verificacion
        mensaje_ascii = self.mensaje.encode('ascii')
        self.mensaje_binario = bitarray()
        self.mensaje_binario.frombytes(mensaje_ascii)

    def agregar_ruido(self):
        # Ruido
        mensaje_ruidoso = ''
        for bit in self.mensaje_binario.to01():
            num_random = random.randint(0, 100)
            if num_random in [i for i in range(0, self.probabilidad)]:
                bit = '0' if bit == '1' else '1'
            mensaje_ruidoso += str(bit)
        self.mensaje_ruidoso = bitarray(mensaje_ruidoso)

    def enviar_objeto(self):
        # Transmision
        self.socket = socket.socket()
        self.socket.connect((self.localhost_ip, self.port))
        self.socket.send(self.mensaje_ruidoso)
        self.socket.close()


emisor = Emisor()

while True:
    emisor.enviar_cadena()
    emisor.enviar_cadena_segura()
    emisor.agregar_ruido()
    emisor.enviar_objeto()
