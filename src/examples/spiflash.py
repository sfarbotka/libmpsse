#!/usr/bin/env python

from mpsse import *
from time import sleep

class SPIFlash:

	WCMD = "\x02"		# Standard SPI flash write command (0x02)
	RCMD = "\x03"		# Standard SPI flash read command (0x03)
	WECMD = "\x06"		# Standard SPI flash write enable command (0x06)
	CECMD = "\xc7"		# Standard SPI flash chip erase command (0xC7)
	
	ADDRESS_LENGTH = 3	# Normal SPI flash address length (24 bits, aka, 3 bytes)
	BLOCK_SIZE = 256	# SPI block size, writes must be done in multiples of this size
	PP_PERIOD = .025	# Page program time, in seconds

	def __init__(self, speed=SIX_MHZ):
	
		self.flash = MPSSE(SPI0, speed, MSB)
		self.chip = self.flash.GetDescription()
		self.speed = self.flash.GetClock()

	def _addr2str(self, address):
        	addr_str = ""

        	for i in range(0, self.ADDRESS_LENGTH):
        	        addr_str += chr((address >> (i*8)) & 0xFF)

        	return addr_str[::-1]

	def Read(self, count, address=0):
		data = None

		self.flash.Start()
		self.flash.Write(self.RCMD + self._addr2str(address))
		data = self.flash.Read(count)
		self.flash.Stop()

		return data

	def Write(self, data, address=0):
		count = 0

		while count < len(data):

			self.flash.Start()
        		self.flash.Write(self.WECMD)
        		self.flash.Stop()

			self.flash.Start()
			self.flash.Write(self.WCMD + self._addr2str(address) + data[address:address+self.BLOCK_SIZE])
			self.flash.Stop()

			sleep(self.PP_PERIOD)
			address += self.BLOCK_SIZE
			count += self.BLOCK_SIZE

	def Erase(self):
		self.flash.Start()
		self.flash.Write(self.WECMD)
		self.flash.Stop()

		self.flash.Start()
		self.flash.Write(self.CECMD)
		self.flash.Stop()

	def Close(self):
		self.flash.Close()


if __name__ == "__main__":

	import sys
	from getopt import getopt as GetOpt, GetoptError

	def usage():
		print ""
		print "Usage: %s [OPTIONS]" % sys.argv[0]
		print ""
		print "\t-r, --read=<file>      Read data from the chip to file"
		print "\t-w, --write=<file>     Write data from file to the chip"
		print "\t-s, --size=<int>       Set the size of data to read/write"
		print "\t-a, --address=<int>    Set the starting address for the read/write operation [0]"
		print "\t-f, --frequency=<int>  Set the SPI clock frequency, in hertz [6,000,000]"
		print "\t-e, --erase            Erase the entire chip"
		print "\t-h, --help             Show help"
		print ""

		sys.exit(1)

	def main():
		file = None
		freq = None
		size = None
		action = None
		address = 0

		try:
			opts, args = GetOpt(sys.argv[1:], "f:s:a:r:w:eh", ["frequency=", "size=", "address=", "read=", "write=", "erase", "help"])
		except GetoptError, e:
			print e
			usage()

		for opt, arg in opts:
			if opt in ('-f', '--frequency'):
				freq = int(arg)
			elif opt in ('-s', '--size'):
				size = int(arg)
			elif opt in ('-a', '--address'):
				address = int(arg)
			elif opt in ('-r', '--read'):
				action = "read"
				file = arg
			elif opt in ('w', '--write'):
				action = "write"
				file = arg
			elif opt in ('-e', '--erase'):
				action = "erase"
			elif opt in ('-h', '--help'):
				usage()

		if action is None:
			print "Please specify an action!"
			usage()

		spi = SPIFlash(freq)
		print "%s initialized at %d hertz" % (spi.chip, spi.speed)

		if action == "read":
			if file is None or size is None:
				print "Please specify an output file and read size!"
				usage()
			
			print "Reading %d bytes starting at address 0x%X..." % (size, address)
			open(file, 'wb').write(spi.Read(size, address))
			print "Data saved to %s" % file
		
		elif action == "write":
			if file is None:
				print "Please specify an input file!"
				usage()

			data = open(file, 'rb').read()
			if size is None:
				size = len(data)

			print "Writing %d bytes from %s to the chip starting at address 0x%X..." % (size, file, address)
			spi.Write(data[0:size], address)
			print "Done."

		elif action == "erase":
			
			print "Erasing entire chip..."
			spi.Erase()
			print "Done."

		spi.Close()

	main()

