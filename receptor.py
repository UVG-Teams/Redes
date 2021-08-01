import socket
from bitarray import bitarray


class Receptor(object):

    def __init__(self, socket):
        self.mensaje = None
        self.mensaje_ruidoso = None
        self.socket = socket

    def recibir_objeto(self):
        # Transmision
        # self.mensaje_ruidoso = mensaje_ruidoso
        c, addr = self.socket.accept()
        print("Got connection from", addr)
        self.mensaje_ruidoso = c.recv(1024)
        c.close()

    def codificacion(self):
        # Codificacion
        self.mensaje = self.mensaje_ruidoso

    def recibir_cadena_segura(self):
        # Verificacion
        mensaje = bitarray()
        mensaje.frombytes(self.mensaje)
        try:
            self.mensaje = mensaje.tobytes().decode('ascii')
        except:
            self.mensaje = "Imposible decodificar"


    def recibir_cadena(self):
        # Aplicacion
        print(self.mensaje)


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
