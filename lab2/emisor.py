import socket
import random
import pickle
import hamming
from message import Message
from bitarray import bitarray


class Emisor(object):

    def __init__(self):
        self.socket = None
        self.localhost_ip = "localhost"
        self.port = 80
        self.probabilidad = 1
        self.mensaje = None
        self.mensaje_codificado = None
        self.mensaje_ruidoso = None
        self.message = None
        self.alg = 'fletcher'
        # self.alg = 'hamming'
        self.posibles_mensajes = [
            'hola',
            'como estas?',
            'adios',
            'que hubo',
            'que tal?',
            'como has estado?',
            'que onda?',
            'ola k ase',
            'dinosaurio',
            'hercules',
            'supercalifrajilisticoespialidoso',
            'heracles',
            'cartas',
            'magia',
            'computadora',
            'apple',
            'lluvia',
            'redes',
        ]

    def enviar_cadena(self):
        # Aplicacion
        # self.mensaje = input("Escriba el mensaje que desea enviar: ")
        self.mensaje = random.choice(self.posibles_mensajes)

    def enviar_cadena_segura(self):
        # Verificacion
        mensaje_ascii = self.mensaje.encode('ascii')
        self.mensaje_codificado = bitarray()
        self.mensaje_codificado.frombytes(mensaje_ascii)
        self.message = Message()
        if self.alg == 'fletcher':
            self.message.verificador = self.fletcher32(self.mensaje_codificado.to01())
        elif self.alg == 'hamming':
            self.mensaje_codificado = self.hamming_alg(self.mensaje_codificado.to01())

    def agregar_ruido(self):
        # Ruido
        mensaje_ruidoso = ''
        for bit in self.mensaje_codificado.to01():
            num_random = random.randint(0, 100)
            if num_random in [i for i in range(0, self.probabilidad)]:
                bit = '0' if bit == '1' else '1'
            mensaje_ruidoso += str(bit)
        self.mensaje_ruidoso = bitarray(mensaje_ruidoso)

    def enviar_objeto(self):
        # Transmision
        self.socket = socket.socket()
        self.socket.connect((self.localhost_ip, self.port))

        self.message.text = self.mensaje_ruidoso
        mensaje_serializado = pickle.dumps(self.message)

        self.socket.send(mensaje_serializado)
        self.socket.close()

    def hamming_alg(self, message):
        return hamming.encode(bitarray(message))

    def fletcher32(self, message):
        w_len = len(message)
        c0 = 0
        c1 = 0
        x = 0

        while w_len >= 360:
            for i in range (360):
                c0 = c0 + ord(message[x])
                c1 = c1 + c0
                x = x + 1
            c0 = c0 % 65535
            c1 = c1 % 65535
            w_len = w_len - 360

        for i in range (w_len):
            c0 = c0 + ord(message[x])
            c1 = c1 + c0
            x = x + 1
        c0 = c0 % 65535
        c1 = c1 % 65535
        return (c1 << 16 | c0)


emisor = Emisor()

while True:
    emisor.enviar_cadena()
    emisor.enviar_cadena_segura()
    emisor.agregar_ruido()
    emisor.enviar_objeto()
