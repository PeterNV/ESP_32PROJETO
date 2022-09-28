import network
import time
import usocket as socket
from machine import Pin
from math import log
import gc
import dht 
gc.collect()
sensor = dht.DHT22(Pin(27))
def obter_arquivo(arquivo):
    conteudo = ''
    a = open(arquivo,'rb')
    conteudo = a.read()
    return conteudo
estacao = network.WLAN(network.STA_IF)
estacao.active(True)
estacao.connect("Wokwi-GUEST","")
while estacao.isconnected() == False:
    pass
print('Conexao realizada')
print(estacao.ifconfig()[0])
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5)
try:
    while True:
        conexao, endereco = s.accept()
        #print('Conexao de %s' % str(endereco))
        requisicao = conexao.recv(1024)
        requisicao = str(requisicao)
        #print('Conteudo = %s' % requisicao)
        sensor.measure()
        
        #hum = sensor.humidity()
        #print(temp)
        if requisicao.find('obter/temperatura') != -1:
            temp = sensor.temperature()
            html = str(round(temp,1))
        elif requisicao.find('obter/umidade') != -1:
            hum = sensor.humidity()
            html = str(round(hum,0))
        elif requisicao.find('/') != -1:
            html = obter_arquivo('http-termistor.txt')
        conexao.send('HTTP/1.1 200 OK\n')
        conexao.send('Content-Type: text/html\n')
        conexao.send('Connection: close\n\n')
        conexao.sendall(html)
        conexao.close()
except KeyboardInterrupt:
    s.close()
    estacao.active(False)