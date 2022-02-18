#!/usr/bin/env python
# coding: UTF-8

#################################################################
# Copyright (C) 2017 Mono Wireless Inc. All Rights Reserved.    #
# Released under MW-SLA-*J,*E (MONO WIRELESS SOFTWARE LICENSE   #
# AGREEMENT).                                                   #
#################################################################

# ライブラリのインポート
import sys
import os
import threading
import time
import datetime
from optparse import *

# WONO WIRELESSのシリアル電文パーサなどのAPIのインポート
sys.path.append('./MNLib/')
from apppal import AppPAL

# ここより下はグローバル変数の宣言
# コマンドラインオプションで使用する変数
options = None
args = None

# 各種フラグ
bEnableLog = False
bEnableErrMsg = False

# プログラムバージョン
Ver = "1.0.0"

def ParseArgs():
	global options, args

	parser = OptionParser()
	if os.name == 'nt':
		parser.add_option('-t', '--target', type='string', help='target for connection', dest='target', default='COM3')
	else:
		parser.add_option('-t', '--target', type='string', help='target for connection', dest='target', default='/dev/ttyUSB0')

	parser.add_option('-b', '--baud', dest='baud', type='int', help='baud rate for serial connection.', metavar='BAUD', default=115200)
	parser.add_option('-s', '--serialmode', dest='format', type='string', help='serial data format type. (Ascii or Binary)',  default='Ascii')
	parser.add_option('-l', '--log', dest='log', action='store_true', help='output log.', default=False)
	parser.add_option('-e', '--errormessage', dest='err', action='store_true', help='output error message.', default=False)
	(options, args) = parser.parse_args()


if __name__ == '__main__':
	print("*** MONOWIRELESS App_PAL_Viewer " + Ver + " ***")

	ParseArgs()

	bEnableLog = options.log
	bEnableErrMsg = options.err
	try:
		PAL = AppPAL(port=options.target, baud=options.baud, tout=0.05, sformat=options.format, err=bEnableErrMsg)
	except:
		print("Cannot open \"AppPAL\" class...")
		exit(1)

	while True:
		try:
			# データがあるかどうかの確認
			if PAL.ReadSensorData():
				# あったら辞書を取得する
				Data = PAL.GetDataDict()

				# なにか処理を記述する場合はこの下に書く
				print(Data)			# 受け取った辞書をそのまま標準出力する

				# ログを出力するオプションが有効だったらログを出力する。
				if bEnableLog == True:
					PAL.OutputCSV()	# CSVでログをとる

		# Ctrl+C でこのスクリプトを抜ける
		except KeyboardInterrupt:
			break

	del PAL

	print("*** Exit App_PAL Viewer ***")