import socket
import time
import sqlite3 as sql

#sql
########################################
db_file = "project.sqlite"

create_station ="""
 CREATE TABLE IF NOT EXISTS station_status (
	station_id INT,
	last_date TEXT,
	alarm1 INT,
	alarm2 INT,
	PRIMARY KEY(station_id) );
"""
select_all_stations = """
SELECT rowid, *
FROM station_status;
"""

insert_station = """
INSERT INTO station_status VALUES
(?, ?, ?, ?);
"""

check_station_existent = """
SELECT rowid, *
FROM station_status
WHERE station_id == ?;
"""

with sql.connect(db_file) as conn:
    conn.execute(create_station)

########################################


# client class

class Client:
    def __init__(self, socket=None, ip=None, port=None):
        self.socket = socket
        self.ip = ip
        self.port = port


## MAIN ##
try:
    # server preperation

    #ip = input("set ip address bind:")
    ip="0.0.0.0"
    #port = int(input("set port bind:"))
    port=8080
    s = socket.socket()
    s.bind((ip, port))
    s.listen(10)
    s.settimeout(0.1)
    client_list = []

    server_messages = ""
    something_changed = True

    # server loop
    while True:
        if something_changed:
            print("listening on ", ip, ":", port)
            if len(client_list) == 0:
                print("\tthere are no client connected\t")
            else:
                for i, client in enumerate(client_list):
                    print("%d) %s:%d" % (i, client.ip, client.port))
            print()
            print(server_messages)
            something_changed = False

        c = None
        try:
            c = s.accept()

        except socket.error:
            pass

        if c != None:
            c = Client(socket=c[0], ip=c[1][0], port=c[1][1])
            c.socket.settimeout(0.1)
            client_list.append(c)
            something_changed = True
            server_messages = "client accepted"

        for client in list(client_list):
            cs = client.socket
            message = None


            try:

                print(client.ip, client.port)
                time.sleep(1)
                cs.send(str("ka").encode())

                message = cs.recv(1024).decode()

                # empty string on recv --> client closed
                if message == "":
                    client_list.remove(client)
                    server_messages = "{}:{} has disconnected.".format(client.ip, client.port)
                    something_changed = True
                    continue

                words = message.split()
                sid = (words[0])
                date = (words[1])
                hour = (words[2])
                alarm1 = (words[3])
                alarm2 = (words[4])

                last_date=date+hour
                sid=int(sid)

                cunn = conn.execute(check_station_existent, (sid,))
                stations = cunn.fetchall()

                if stations:
                    cunn.execute("DELETE FROM station_status WHERE station_id==%d" % sid)
                    cunn.execute(insert_station, (sid, last_date, alarm1, alarm2))
                else:
                    cunn.execute(insert_station, (sid, last_date, alarm1, alarm2))

                print("sid:",sid)
                print("date:",date)
                print("hour:",hour)
                print("alarm1:",alarm1,"  alarm2:",alarm2)
                print()
            except socket.error:
                message = None



except KeyboardInterrupt:
    pass
finally:

    print()
    print("closing server socket")
    s.close()
    print("goodbye")
