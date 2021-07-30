import socket


def enviar_cadena():
    mensaje = input("Escriba el mensaje que desea enviar: ")
    return enviar_cadena_segura(mensaje)


def enviar_cadena_segura(mensaje):
    return agregar_ruido(mensaje)


def agregar_ruido(mensaje):
    mensaje_ruidoso = mensaje
    return enviar_objeto(mensaje_ruidoso)


def enviar_objeto(mensaje_ruidoso):
    return mensaje_ruidoso



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
        enviar_cadena()

        s = socket.socket()
        localhost_ip = "localhost"
        port = 80

        s.connect((localhost_ip, port))

        print(s.recv(1024))
        s.close()

    else:
        pass
