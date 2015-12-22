#!/usr/bin/env python
"""
Rutina que permite el calculo de PPSD para una traza adquirida por Seiscomp o por EW
"""
from obspy import read, UTCDateTime
from obspy.fdsn.client import Client as ClientFDSN
from obspy.earthworm import Client as ClientEW
from obspy.xseed import Parser
from obspy.signal import PPSD
import progressbar
import time
import sys

#############funciones###########################################################
ip_fdsn = "http://10.100.100.232:8091"
ip_ew = ["10.100.100.229", 21666]
def Client(server):
	if  server == 'fdsn':
		client = ClientFDSN(ip_fdsn)
	elif server == 'ew': 
		client = ClientEW(ip_ew[0], ip_ew[1])
	return client
def waveform(server, client, network, station, location, channel, t1, t2):
	if server == 'fdsn':
		st = client.get_waveforms(network, station, location, channel, t1, t2)
	elif server == 'ew':
		st = client.getWaveform(network, station, location, channel, t1, t2)
	return st
		


#######################ingreso de parametros########################################
server_input = raw_input("Ingrese el nombre del servidor (Earthworm = 0 / SEISCOMP = 1)\n")
station_input = raw_input("Ingrese la informacion del canal. Ej: CM RUS 00 HHZ\n")
time1_input = raw_input("Ingrese tiempo inicial. Ej: yyyy mm dd hh mm\n")
time2_input = raw_input("Ingrese tiempo final.\n" )
dataless_q = raw_input("Desea usar un dataless particular? [s/n]\n")
if dataless_q == "s":
	dataless_path = raw_input("Ingrese la ruta del dataless:\n")
elif dataless_q == "n":
	dataless_path = '/bd/seismo/dataless'
	print dataless_path
info = station_input.split(' ')
time1 = time1_input.split(' ')
time2 = time2_input.split(' ')
network, station, location, channel = info[0], info[1], info[2], info[3]
t1 = UTCDateTime(int(time1[0]), int(time1[1]), int(time1[2]), int(time1[3]), int(time1[4]))
t2 = UTCDateTime(int(time2[0]), int(time2[1]), int(time2[2]), int(time2[3]), int(time2[4]))


#######################query#########################################################
if server_input == '0':
	client = Client('ew')
	print client
	st = waveform('ew', client, network, station, location, channel, t1, t2)
elif server_input == '1':
	client = Client('fdsn')
	print client
	st = waveform('fdsn', client, network, station, location, channel, t1, t2)
else:
	print "Servidor no valido"
	sys.exit()

print st
#######################Calculo de la PPSD###########################################

dataless = dataless_path+'/'+network+'.'+station+'..HH.dataless'
print dataless
parser = Parser(dataless)
paz = parser.getPAZ(st[0].id)
#print paz
ppsd = PPSD(st[0].stats, paz)
ppsd.add(st)
ppsd.plot()



 
