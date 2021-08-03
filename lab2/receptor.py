import socket
import pickle
import hamming
from message import Message
from bitarray import bitarray
import matplotlib.pyplot as plt


class Receptor(object):

    def __init__(self, socket):
        self.socket = socket
        self.mensaje = None
        self.mensaje_serializado = None
        self.mensaje_ruidoso = None
        self.mensaje_binario = None
        self.mensaje_corregido = None
        self.message = None
        self.alg = 'fletcher'
        # self.alg = 'hamming'
        self.efectividad = []

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
        if self.alg == 'fletcher':
            if self.fletcher32(self.mensaje_binario) != self.message.verificador:
                try:
                    print("Mensaje con ruido, corrigiendo...")
                    print(bitarray(self.mensaje_binario).tobytes().decode('ascii'))
                    self.corregir_errores()
                    self.mensaje = self.mensaje_corregido
                    self.efectividad.append('Detectado')
                except:
                    self.mensaje_corregido = None
                    self.mensaje = "Imposible de decodificar"
                    self.efectividad.append('Fallido')
            else:
                self.mensaje_corregido = None
                self.mensaje = bitarray(self.mensaje_binario).tobytes().decode('ascii')
                self.efectividad.append('Sin ruido')
        elif self.alg == 'hamming':
            try:
                self.mensaje_binario = self.hamming_alg(self.mensaje_ruidoso).to01()
                self.corregir_errores()
                self.mensaje = self.mensaje_corregido
                self.efectividad.append('Corregido')
            except:
                self.mensaje_corregido = None
                self.mensaje = "Imposible de decodificar"
                self.efectividad.append('Fallido')

    def corregir_errores(self):
        self.mensaje_corregido = bitarray(self.mensaje_binario).tobytes().decode('ascii')

    def recibir_cadena(self):
        # Aplicacion
        print(self.mensaje)

    def hamming_alg(self, message):
        return hamming.decode(message)

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

for i in range(1000):
    receptor.recibir_objeto()
    receptor.codificacion()
    receptor.recibir_cadena_segura()
    receptor.recibir_cadena()


# Graficas
labels = set(receptor.efectividad)
labels_count = {}
sizes = []

for i in labels:
    labels_count[i] = 0

for i in receptor.efectividad:
    labels_count[i] += 1

[sizes.append(int(i)) for i in labels_count.values()]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
plt.show()
input()
