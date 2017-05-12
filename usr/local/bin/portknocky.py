#! /usr/bin/env python


#Portknocky, by Markus Bawidamann, written D20170501, see command line help for more info

import socket, errno, time, optparse,sys
import signal

def timestamp(ts):
	if ts == True:
		return time.strftime("D%Y%m%d_T%H%M%S")


def stats():
	timestamp_now = time.time()
	print "Connection statistics:"
	print "-----------------------"
	print "Total runtime: " + str(round((timestamp_now - timestamp_start)/60,2)) + " minutes"
	print "Total connection attempts: " + str(i)
	print "		of them successes: " + str(conok)
	print "		Connection refused: " + str(conref)
	print "		Connection timed out: " +str(contimeout)
	print "		No address associated with hostname: " +str(condns)
	print "		No route to host: " + str(ehostunreach)

def signal_handler(signal, frame):
	
	print "Interrupted/terminated"
	stats()

	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


timestamp_start = time.time()


parser = optparse.OptionParser()

parser.add_option('-D', '--timestamp', 	action="store_true", dest="timestamp", help="Shows timestamp for every connection attempt, in the format D[date] T[time]. Default is on", default=True)
parser.add_option("-i", "--interval", type="int", action="store", dest="interval", help="Interval in seconds in which the connections happen. Default is 30 seconds", default="30")
parser.add_option("-t", "--duration", type="float", action="store", dest="duration", help="How long the test should run, given in hours. Default is 1", default="1")
parser.add_option("-p", "--port", type="int", action="store", dest="port", help="Which port to connect for the port ping. Default is 22", default="22")
parser.usage="%prog [options] hostname\n\nThis tool allows to test port connectivity on a host by connecting to the specified port every x seconds defined in interval and reporting the result of it. \nTool will show statistics of success/failure at the end of the alloted run time.\nWritten by Markus Bawidamann D20111014 for the purpose of troubleshooting elusive network connectivity issues."


options, args = parser.parse_args()


if args == []:
	print "You must specify a hostname to ping as an argument!"
	parser.print_help()
	sys.exit(1)
	


total_runtime= options.duration			#total runtime in hours
interval = options.interval				#interval, run the connect test every x seconds
hostname=args[0]
port=options.port


print "Trying to open port " + str(port)+ " on target machine "+ hostname+ ", please wait."
print 
print "Interval of connections:",interval,"seconds"
print "Total runtime: ", total_runtime, " hours"
print "Time stamps: ", options.timestamp
print 
print "info: If port is closed, the response is immediate (connection refused)."
print "If there is a firewall blocking it, it will take more time, as the firewall will likely drop packets (to delay) and report connection timed out"

conref=0
contimeout=0
condns=0
ehostunreach=0
conok=0

runs=int(total_runtime*60*60/interval)

for i in range(1,runs):
	#print "connecting to port "+str(port) + ", run " + str(i)

	try:
		s = socket.socket()         # Create a socket object
		s.connect((hostname, port))
		
	except socket.error as (err, msg):
		if err == 111:
			print timestamp(options.timestamp) +": Connection refused"
			conref = conref + 1
		if err == 110:
			print timestamp(options.timestamp) +": Connection timed out"
			contimeout=contimeout + 1
		if err == -5:	
			print timestamp(options.timestamp) +": No address associated with hostname"
			condns=condns + 1
		if err == 113:
			print timestamp(options.timestamp) +": No route to host"
			ehostunreach = ehostunreach + 1
	except:
		print timestamp(options.timestamp) +": Not handled error, still continuing"
	else:
		conok=conok+1
		print timestamp(options.timestamp) +": OK"
	
	s.close
	time.sleep(interval)

stats()


