#!/usr/bin/python
# coding: UTF-8

import sys
import datetime

from parseFmt_Ascii import FmtAscii
from parseFmt_Binary import FmtBinary

# シリアル読み込みを行うクラス

class MWStdInput:
	def __init__( self, mode='Ascii', rxout=False ):
		self.reinit(mode)

	def __del__(self):
		self.SerialClose()

	def reinit(self, mode='Ascii' ):
		self.mode = mode
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
			self.msg = sys.stdin.buffer.read(1)
			if(len(self.msg) > 0):
				self.count = 0
				self.Fmt.process(self.msg)
				if self.Fmt.is_comp():
					self.bDataArrived = True
					self.receipttime = datetime.datetime.today()
			else:
				self.bDataArrived = False
				self.count += 1
				if self.count > 10:
					print( '! EOF' )
					exit(0)

		elif self.mode == 'Binary':
			if self.ser.inWaiting() > 0:
				while True:
					self.c = ord(sys.stdin.buffer.read(1))
					self.Fmt.process(self.c)
					if self.Fmt.is_comp():
						break
				if self.Fmt.is_comp():
					self.bDataArrived = True
					self.arrivedtime = datetime.datetime.today()
				else:
					self.bDataArrived = False
					self.Fmt.terminate()
			else:
				self.bDataArrived = False
		else:
			return 0

		return 1

	def IsDataArrived(self):
		return self.bDataArrived

	def GetMode(self):
		return self.mode

	def GetCheckSum(self):
		return self.Fmt.get_checksum()

# テスト用コード
if __name__=='__main__':
	fmt = MWStdInput( mode='Ascii' )

	i = 0
	try:
		while True:
			fmt.ReadSerialLine()
			if fmt.IsDataArrived():
				msg = fmt.GetPayload()
				print(msg)
	except KeyboardInterrupt:
		exit(1)
