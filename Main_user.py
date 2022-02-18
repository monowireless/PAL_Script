#!/usr/bin/env python
# coding: UTF-8

#################################################################
# Copyright (C) 2017-2021 Mono Wireless Inc. All Rights Reserved.    #
# Released under MW-SLA-*J,*E (MONO WIRELESS SOFTWARE LICENSE   #
# AGREEMENT).                                                   #
#################################################################

import sys
import datetime

# WONO WIRELESSのシリアル電文パーサなどのAPIのインポート
sys.path.append('./MNLib/')
try:
	from apppal import AppPAL
except ImportError:
	print("Cannot Open MONOWireless library...")
	sys.exit(1)

# この関数に処理したい内容を書く
def Main(PAL=None):
	# 渡された変数がAppPALクラスか確認する。
	if isinstance(PAL, AppPAL):
		sns_data = PAL.GetDataDict()

		# 受信時間
		print('Receive Time: ', end='')
		if isinstance(sns_data['ArriveTime'], datetime.datetime):
			print(sns_data['ArriveTime'].strftime('%Y/%m/%d %H:%M:%S') + '.%03d'%(sns_data['ArriveTime'].microsecond/1000))
		else:
			print(sns_data['ArriveTime'])

		# 論理デバイスID
		print('Logical ID: 0x%02X'%sns_data['LogicalID'])
		# シリアル番号
		print('Serial ID: 0x' + sns_data['EndDeviceSID'])
		# 電源電圧
		print('Power: %d mV' % sns_data['Power'])

		# センサーの名前を調べる
		sname  = PAL.GetSensorName()

		# センサー名がPALだったらパルのモデル名を出力する。
		if sname == 'PAL':
			pid = PAL.GetPALName()
			print('Sensor: ' + pid )
		else:
			print('Sensor: ' + sname )

		# アナログセンサーモード(App_Tag)
		if sname == 'Analog':
			print('ADC1: %d mV'%sns_data['ADC1'])
			print('ADC2: %d mV'%sns_data['ADC2'])
		else:
			# ホールIC
			if 'HALLIC' in sns_data.keys():
				print('HALLIC: %d'%sns_data['HALLIC'])

			# 温度
			if 'Temperature' in sns_data.keys():
				print('Temperature: %.02f degC'%sns_data['Temperature'])

			# 湿度
			if 'Humidity' in sns_data.keys():
				print('Humidity: %.02f %%'%sns_data['Humidity'])

			# 照度
			if 'Illuminance' in sns_data.keys():
				print('Illuminance: %f lux'%sns_data['Illuminance'])

			# 気圧
			if 'Pressure' in sns_data.keys():
				print('Pressure: %f hPa'%sns_data['Pressure'])

			# 加速度
			if 'AccelerationX' in sns_data.keys():
				print('X: ', end='')
				print(sns_data['AccelerationX'])
				print('Y: ', end='')
				print(sns_data['AccelerationY'])
				print('Z: ', end='')
				print(sns_data['AccelerationZ'])

			# ジャイロ
			if 'Roll' in sns_data.keys():
				print('Roll: ', end='')
				print(sns_data['Roll'])
				print('Pitch: ', end='')
				print(sns_data['Pitch'])
				print('Yaw: ', end='')
				print(sns_data['Yaw'])

			# カラーセンサー
			if 'Red' in sns_data.keys():
				print('Red: ', end='')
				print(sns_data['Red'])
				print('Green: ', end='')
				print(sns_data['Green'])
				print('Blue: ', end='')
				print(sns_data['Blue'])
				print('IR: ', end='')
				print(sns_data['IR'])


		print()

