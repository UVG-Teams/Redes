import socket
from bitarray import bitarray


class Receptor(object):

    def __init__(self, socket):
        self.socket = socket
        self.mensaje = None
        self.mensaje_decodificado = None
        self.mensaje_ruidoso = None

    def recibir_objeto(self):
        # Transmision
        # self.mensaje_ruidoso = mensaje_ruidoso
        c, addr = self.socket.accept()
        print("Got connection from", addr)
        self.mensaje_ruidoso = c.recv(1024)
        c.close()

    def codificacion(self):
        # Codificacion
        mensaje = bitarray()
        mensaje.frombytes(self.mensaje_ruidoso)
        try:
            self.mensaje_decodificado = mensaje.tobytes().decode('ascii')
        except:
            self.mensaje_decodificado = "Imposible decodificar"

    def recibir_cadena_segura(self):
        # Verificacion
        self.detectar_errores()
        self.corregir_errores()
        self.mensaje = self.mensaje_corregido

    def recibir_cadena(self):
        # Aplicacion
        print(self.mensaje)

    def detectar_errores(self, algoritmo='fletcher-checksum'):
        if algoritmo == 'fletcher-checksum':
            self.mensaje_analizado = self.mensaje_decodificado
        else:
            self.mensaje_analizado = self.mensaje_decodificado

    def corregir_errores(self, algoritmo='hamming'):
        if algoritmo == 'hamming':
            self.mensaje_corregido = self.mensaje_analizado
        else:
            self.mensaje_corregido = self.mensaje_analizado


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
