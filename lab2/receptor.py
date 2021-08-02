import socket
import pickle
from message import Message
from bitarray import bitarray


class Receptor(object):

    def __init__(self, socket):
        self.socket = socket
        self.mensaje = None
        self.mensaje_serializado = None
        self.mensaje_ruidoso = None
        self.mensaje_binario = None
        self.mensaje_corregido = None
        self.message = None

    def recibir_objeto(self):
        # Transmision
        c, addr = self.socket.accept()
        print("Got connection from", addr)
        self.mensaje_serializado = c.recv(1024)
        c.close()

    def codificacion(self):
        # Codificacion
        self.message = pickle.loads(self.mensaje_serializado)
        self.mensaje_ruidoso = self.message.text
        self.mensaje_binario = self.mensaje_ruidoso.to01()

    def recibir_cadena_segura(self):
        # Verificacion
        if self.fletcher32(self.mensaje_binario) != self.message.verificador:
            try:
                print("Mensaje con ruido, corrigiendo...")
                print(bitarray(self.mensaje_binario).tobytes().decode('ascii'))
                self.corregir_errores()
                self.mensaje = self.mensaje_corregido
            except:
                self.mensaje_corregido = None
                self.mensaje = "Imposible de decodificar"
        else:
            self.mensaje_corregido = None
            self.mensaje = bitarray(self.mensaje_binario).tobytes().decode('ascii')


    def corregir_errores(self):
        self.mensaje_corregido = bitarray(self.mensaje_binario).tobytes().decode('ascii')

    def recibir_cadena(self):
        # Aplicacion
        print(self.mensaje)

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


s = socket.socket()
port = 80

s.bind(("", port))
print ("Socket binded to %s" %(port))

s.listen(5)
print ("Socket is listening")

receptor = Receptor(s)

while True:
    receptor.recibir_objeto()
    receptor.codificacion()
    receptor.recibir_cadena_segura()
    receptor.recibir_cadena()
