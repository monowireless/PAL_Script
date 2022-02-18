#!/usr/bin/python
# coding: UTF-8

import sys
import datetime

from parseFmt_Ascii import FmtAscii
from parseFmt_Binary import FmtBinary

# シリアル出力のログを読み込む

class MWFileRead:
	def __init__( self, mode='Ascii', rxout=False, filename=None ):
		self.reinit(mode, filename)

	def __del__(self):
		self.SerialClose()

	def reinit(self, mode='Ascii', filename=None ):
		self.mode = mode
		self.filename = filename
		self.bDataArrived = False
		self.receipttime = None
		self.count = 0

		self.Fmt = None
		if self.mode == 'Ascii':
			self.Fmt = FmtAscii()
		elif self.mode == 'Binary':
			self.Fmt = FmtBinary()
		else:
			return

		if self.filename == None:
			print('Not Found file...')
			exit(1)

		try:
			self.f = open(self.filename, 'r')
		except:
			print('Connot open this file...')
			exit(1)

		self.lines = self.f.readlines()
		self.f.close()

		self.readlines = len(self.lines)
		self.indexline = 0

	# シリアルポートを検索する。
	def SerialSelect(self, portname=None):
		return

	# シリアルポートを開く
	def SerialOpen(self):
		return True

	# シリアルポートを閉じる
	def SerialClose(self):
		return True

	def SerialWrite(self, Cmd):
		return True

	def GetPayload(self):
		return self.Fmt.get_payload()
	
	def GetReceiptTime(self):
		if self.IsDataArrived():
			return self.receipttime

		return None

	def ReadSerialLine(self):
		self.bDataArrived = False
		if self.mode == 'Ascii':
			line = self.lines[self.indexline].split(' ')
			index = 0
			if len(line) == 1:
				index = 0
				self.receipttime = datetime.datetime.today()
			elif len(line) == 3:
				index = 2
				datestr = line[0][1:] + ' ' + line[1][:-1] + '000'
				print(datestr)
				self.receipttime = datetime.datetime.strptime( datestr, "%Y-%m-%d %H:%M:%S.%f" )

			for c in line[index]:
				self.msg = c
				self.Fmt.process(self.msg)
				if self.Fmt.is_comp():
					self.bDataArrived = True

			self.indexline += 1
			if self.indexline == self.readlines:
				print('EOF!')
				exit(0)

#		elif self.mode == 'Binary':
#			if self.ser.inWaiting() > 0:
#				while True:
#					self.c = ord(sys.stdin.buffer.read(1))
#					self.Fmt.process(self.c)
#					if self.Fmt.is_comp():
#						break
#				if self.Fmt.is_comp():
#					self.bDataArrived = True
#					self.arrivedtime = datetime.datetime.today()
#				else:
#					self.bDataArrived = False
#					self.Fmt.terminate()
#			else:
#				self.bDataArrived = False
		else:
			return 0

		return 1

	def IsDataArrived(self):
		return self.bDataArrived

	def GetMode(self):
		return self.mode

	def GetCheckSum(self):
		return self.Fmt.get_checksum()
