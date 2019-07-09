import socket
import datetime

with socket.socket() as s:
    #ip = input("enter ip:")
    ip="0.0.0.0"
    #port = int(input("enter port:"))
    port=8080
    s.connect((ip, port))

    serverconnect=0

    while True:
        f = open("status2.txt")
        f.readline(15)                  # read "station number:"
        sid = str(f.readline(8))        #read  the true station number
        now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M")
        f.readline(7)                   # read "alarm1:"
        alarm1=str(f.readline(2))       # read the true alarm
        f.readline(7)                   # read "alarm2:"
        alarm2=str(f.readline(2))       # read the true alarm
        f.closed

        status = sid," ", now+" ", alarm1," " , alarm2
        status=''.join(status)          #make status str
        status=status.replace('\n','')  #replace \n to space

        ka = s.recv(1024).decode()      #receive the signal to send
        if ka=="ka":
            print(status)
            print("signal was resive")
            s.send(status.encode())
            serverconnect=0;
        else:
            serverconnect+=1

        if(serverconnect==10):
            break


    print("goodbye")
