import socket

# --> Configuración del servidor
HOST = '127.0.0.1'
PORT = 12345

# --> Nombre del archivo a enviar
file_name = 'imagen.jpg'

# --> Iniciar conexión UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    # --> Leer el archivo y obtener su tamaño
    with open(file_name, 'rb') as file:
        file_data = file.read()
        file_size = len(file_data)

    # --> Enviar el nombre del archivo y su tamaño
    client_socket.sendto(f"{file_name}:{file_size}".encode(), (HOST, PORT))

    # --> Enviar el archivo en fragmentos
    bytes_sent = 0
    while bytes_sent < file_size:
        # --> Enviar fragmentos de 1024 bytes
        bytes_to_send = min(1024, file_size - bytes_sent)

        # --> Enviar el fragmento de archivo
        client_socket.sendto(file_data[bytes_sent:bytes_sent + bytes_to_send], (HOST, PORT))

        # Esperar la confirmación del servidor
        confirmation, _ = client_socket.recvfrom(1024)
        if not confirmation:
            break
        else:
            bytes_sent += bytes_to_send
            print(f"Enviados {bytes_sent} de {file_size} bytes.")

    print(f"Archivo '{file_name}' enviado con éxito.")