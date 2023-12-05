import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))

# Récupération d'une string utilisateur
msg = input("Entrez une string : ")

if "+" in msg:
    num1, op, num2 = msg.partition("+")
elif "-" in msg:
    num1, op, num2 = msg.partition("-")
elif "*" in msg:
    num1, op, num2 = msg.partition("*")

if int(num1) > 4294967295 or int(num2) > 4294967295:
    print("Nombre trop grand")
    exit()

if op == "+":
    op = b"00"
elif op == "-":
    op = b"01"
elif op == "*":
    op = b"10"

num1 = num1.encode()
num2 = num2.encode()

msg = op + len(num1).to_bytes(2, byteorder='big') + num1 + b"0" + len(num2).to_bytes(2, byteorder='big') + num2 + b"0"
# On envoie
s.send(msg)

# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())
s.close()
