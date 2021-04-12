import time
import BaseHTTPServer
import os

#Dados que não são atualizados constantemente
   
model_name_Proc=os.popen('grep "model name" /proc/cpuinfo').read()  
version=os.popen('grep PRETTY_NAME /etc/os-release').read() 

#Comecando servidor
HOST_NAME = '192.168.1.10' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000

def UsedSpace():
	espaco_livre=os.popen('grep MemFree /proc/meminfo').read().split(':')[1]
	cached=os.popen('grep Cached /proc/meminfo').read().split(':')[1]
	buffered=os.popen('grep Buffers /proc/meminfo').read().split(':')[1]
	result=int(espaco_livre[:espaco_livre.index('k')])+int(cached[:cached.index('k')])+int(buffered[:buffered.index('k')])
	return str(result)+" kB"
 
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Trabalho de SisOp 1</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        s.wfile.write("<p> Data e Hora:%s</p>"%os.popen('date').read())
        s.wfile.write("<p> Uptime:%s</p>"%os.popen('uptime -p').read()[2:])
        s.wfile.write("<p>Modelo:%s</p>"%model_name_Proc.split("model name\t:")[1])
        s.wfile.write("<p>Velocidade:%s</p>"%os.popen('grep "cpu MHz" /proc/cpuinfo').read().split(':')[1])
        s.wfile.write("<p>Memoria RAM Total:%s</p>"%os.popen('grep MemTotal /proc/meminfo').read().split(":")[1])
        s.wfile.write("<p>Espaco Ocupado:%s</p>"%UsedSpace())
        s.wfile.write("<p>Versao sistema:%s</p>"%version.split("PRETTY_NAME=")[1][1:len(version.split("PRETTY_NAME=")[1])-2]) 
        
        #Aqui eu faco a lista de processos
        s.wfile.write("<p>Lista de processos em execucao:<br>%s</p>"%os.popen('ps').read().replace("\n","<br>"))
         

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

