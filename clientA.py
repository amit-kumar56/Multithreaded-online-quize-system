import socket 
from threading import Thread 
import sqlite3 as sql

#from SocketServer import ThreadingMixIn 

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print ("[+] New server socket thread started for " + ip + ":" + str(port) )
 
    def run(self): 
        
        data=conn.recv(500000).decode()
        print(data)
        if data=='send answers':
            with sql.connect("m.db") as conn1 :
                conn1.row_factory = sql.Row
                curr = conn1.cursor()    
                curr.execute("SELECT answers FROM sents")
                query=curr.fetchall()
                x=len(query)
                ans=''
                j=1
                for i in range(x):
                    ans+=str(j)+'.'+query[i][0]+'::'
                    j=j+1
                conn.send(ans.encode())
                conn1.close()
        elif data=='send questions':
            with sql.connect("m.db") as conn1 :
                conn1.row_factory = sql.Row
                curr = conn1.cursor()    
                curr.execute("SELECT questions FROM sents")
                query=curr.fetchall()
                x=len(query)
                qest=''
                j=1
                for i in range(x):
                    qest+=str(j)+' . '+query[i][0]+'::'
                    j=j+1
                conn.send(qest.encode())
                conn1.close()
        else:
            with sql.connect("m.db") as conn1 :
                conn1.row_factory = sql.Row
                curr = conn1.cursor()    
                query = "INSERT INTO sents (questions,answers) VALUES (?,?)"
                lst=data.split('::')
                for i in lst:
                    x=i.split(':')
                    questions=x[0]
                    answers=x[1]
                    #print(questions,answers)
                
                    values=(questions,answers)
                    curr.execute(query, values)
                    conn1.commit()
                conn1.close()
            #con.close()
            
            
            

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2004 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 

while True: 
    tcpServer.listen(4) 
    print ("Multithreaded Python server : Waiting for connections from TCP clients..." )
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 
