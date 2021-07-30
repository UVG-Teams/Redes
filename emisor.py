import socket




class Emisor(object):

    def __init__(self):
        self.mensaje = ''
        self.mensaje_ruidoso = ''

    def enviar_cadena(self):
        self.mensaje = input("Escriba el mensaje que desea enviar: ")

    def enviar_cadena_segura(self):
        return self.mensaje

    def agregar_ruido(self):
        pass

    def enviar_objeto(self):
        return self.mensaje_ruidoso


emisor = Emisor()

while True:
    print("Menu:")
    opcion = int(input("""
    1. Escribir mensaje
    2. Enviar mensaje
    0. Salir
    """))

    if opcion == 0:
        print("Bye")
        exit()
    elif opcion == 1:
        emisor.enviar_cadena()
    elif opcion == 2:
        s = socket.socket()
        localhost_ip = "localhost"
        port = 80

        s.connect((localhost_ip, port))

        s.send(b'HOLA')

        s.close()
    else:
        pass
