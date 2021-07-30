import socket


def recibir_objeto(mensaje_ruidoso):
    return recibir_cadena_segura(mensaje_ruidoso)


def codificacion(mensaje_ruidoso):
    mensaje = mensaje_ruidoso
    return recibir_cadena_segura(mensaje)


def recibir_cadena_segura(mensaje):
    return recibir_cadena(mensaje)


def recibir_cadena(mensaje):
    return mensaje


s = socket.socket()
port = 80

s.bind(("", port))
print ("Socket binded to %s" %(port))

s.listen(5)
print ("Socket is listening")

while True:
    c, addr = s.accept()

    print("Got connection from", addr)
    print(c.recv(1024))

    c.close()
