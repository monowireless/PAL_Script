#!/usr/bin/env python
# coding: UTF-8

#################################################################
# Copyright (C) 2017 Mono Wireless Inc. All Rights Reserved.    #
# Released under MW-SLA-*J,*E (MONO WIRELESS SOFTWARE LICENSE   #
# AGREEMENT).                                                   #
#################################################################

# ライブラリのインポート
import sys
from optparse import *

# WONO WIRELESSのシリアル電文パーサなどのAPIのインポート
sys.path.append('./MNLib/')
try:
	from apppal import AppPAL
except ImportError:
	print("Cannot Open MONOWireless library...")
	sys.exit(1)

# ここより下はグローバル変数の宣言
# コマンドラインオプションで使用する変数
options = None
args = None

# 各種フラグ
bEnableLog = False
bEnableErrMsg = False

# プログラムバージョン
Ver = "1.2.0"

def mainloop(PAL):

	try:
		from Main_user import Main
	except:
		mainflag = False
	else:
		mainflag = True

	if PAL.ReadSensorData():
		if mainflag:
			Main(PAL)
		else:
			PAL.ShowSensorData()


def ParseArgs():
	global options, args

	parser = OptionParser()
	parser.add_option('-t', '--target', type='string', help='target for connection', dest='target', default=None)
	parser.add_option('-b', '--baud', dest='baud', type='int', help='baud rate for serial connection.', metavar='BAUD', default=115200)
	parser.add_option('-s', '--serialmode', dest='format', type='string', help='serial data format type. (Ascii or Binary)',  default='Ascii')
	parser.add_option('-l', '--log', dest='log', action='store_true', help='output log.', default=False)
	parser.add_option('-e', '--errormessage', dest='err', action='store_true', help='output error message.', default=False)
	parser.add_option('-i', '--standardinput', dest='stdinp', action='store_true', help='Use standard input.', default=False)
	parser.add_option('-f', '--file', type='string', help='Read Serial logfile', dest='file', default=None)
	(options, args) = parser.parse_args()

if __name__ == '__main__':
	print("*** MONOWIRELESS App_PAL_Viewer " + Ver + " ***")

	ParseArgs()

	bEnableLog = options.log
	bEnableErrMsg = options.err
	try:
		PAL = AppPAL(port=options.target, baud=options.baud, tout=0.05, sformat=options.format, autolog=bEnableLog, err=bEnableErrMsg, stdinput=options.stdinp, Logfilename=options.file)
	except:
		print("Cannot open \"AppPAL\" class...")
		exit(1)

	while True:
		try:
			mainloop(PAL)
		except KeyboardInterrupt:
			break

	del PAL

	print("*** Exit App_PAL Viewer ***")