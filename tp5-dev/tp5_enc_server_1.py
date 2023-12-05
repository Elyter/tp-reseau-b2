import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9999))  

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        # On reçoit la string Hello du client
        op = conn.recv(2)
        if op == b"00":
            op = b"+"
        elif op == b"01":
            op = b"-"
        elif op == b"10":
            op = b"*"

        header = conn.recv(2)
        
        num1len = int.from_bytes(header, byteorder='big')

        num1 = conn.recv(num1len)

        print(f"{header} {num1len} {num1}")

        if conn.recv(1) != b"0":
            print("Erreur de format")
            break

        header = conn.recv(2)

        num2len = int.from_bytes(header, byteorder='big')

        num2 = conn.recv(num2len)

        if conn.recv(1) != b"0":
            print("Erreur de format")
            break


        print(f"Données reçues du client : {num1.decode()}{op.decode()}{num2.decode()}")
        print(f"Données reçues en bytes : {num1}{op}{num2}")
        print(f"Résultat : {eval(num1.decode() + op.decode() + num2.decode())}")

        # On envoie le résultat au client
        conn.send(str(eval(num1.decode() + op.decode() + num2.decode())).encode())
        
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
