from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
from werkzeug import secure_filename
import socket 
from threading import Thread 
#from SocketServer import ThreadingMixIn 
import socket

import xlrd
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
@app.route('/change',methods = ['POST','GET'])
def saveThread():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        book = xlrd.open_workbook(f.filename)
        sheet = book.sheet_by_name("Sheet1")

        host = '0.0.0.0' 
        port = 2004
        BUFFER_SIZE = 2000 
        tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcpClientA.connect((host, port))
        
        #print('got connection from ',add)
        #tcpClientA.sendfile(sheet)
        i=1
        x=''
        while i<sheet.nrows:
            msg1=sheet.cell(i,0).value
            ans=sheet.cell(i,1).value
            x+=str(msg1)+':'+str(ans)+'::'
            
            i=i+1
        tcpClientA.send(x.encode())  
        tcpClientA.close()
        return render_template('index.html',ms='questions uploaded')
        
@app.route("/cnquestions")
def qustionsThread():
    host = '0.0.0.0' 
    port = 2004
    #BUFFER_SIZE = 2000 
    tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcpClientB.connect((host, port))
    msg="send questions"
    tcpClientB.send(msg.encode())
    rows=tcpClientB.recv(50000).decode()
    #print(rows)


    return render_template('cnquestions.html',rows=rows)
@app.route('/cnresult',methods = ['POST', 'GET'])
def resultThread():
    if request.method == 'POST':
        result = request.form
        #nm=request.form['xx']
        #print(result)
        host = '0.0.0.0' 
        port = 2004
        #BUFFER_SIZE = 2000 
        tcpClientC = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcpClientC.connect((host, port))
        msg="send answers"
        tcpClientC.send(msg.encode())
        rows=tcpClientC.recv(50000).decode()
        #print(rows)
        x=result
        y=rows.split('::')
        cor=0
        wor=0
        lst=[]
        for i ,z in x.items():
            lst.append(z)
        for i,j in zip(lst,y):
            if i==j.split('.')[1]:
                cor=cor+1
            else:
                wor=wor+1    
        #print(cor, wor)           
        return render_template("cnresult.html",result=result,rows=rows, cor=cor,wor=wor)
    else:
        return render_template('index.html')

   

if __name__ == '__main__' :
    app.run(debug=True)