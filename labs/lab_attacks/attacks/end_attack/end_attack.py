#
#
# Copyright (c) 2020 Adrian Campazas Vega, Ignacio Samuel Crespo Martinez, Angel Manuel Guerrero Higueras.
#
# This file is part of DOROTHEA 
#
# DOROTHEA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DOROTHEA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from attacks.celery import app
from pexpect import pxssh
import nmap
import os
import random
import time
import subprocess as sp
import time


def end_attack():
	send_end_attack('140.30.20.4', 'root', 'password','/checkReceiver.txt')
	send_end_attack('140.30.20.3', 'root', 'password','/checkNetflow.txt')
	send_end_attack('152.148.48.2', 'root', 'password','/checkRouter.txt')
	check_data_saved()
	print("Data stored correctly, shutting down system")
	#closing labs




def check_data_saved():    
	while (True):
		time.sleep(10)
		checkReceiver = sp.getoutput("cat /checkAttackerReceiver.txt")
		chechRouter = sp.getoutput("cat /checkAttackerRouter.txt")
		checkNetflow = sp.getoutput("cat /checkAttackerNetflow.txt")
		if checkReceiver == "2" and chechRouter == "2" and checkNetflow == "2":
			break 



def send_end_attack(ip,user,password,file):
	#We modify the check of the router and the slave so that they generate the csv
	s = pxssh.pxssh()
	if not s.login (ip, user, password):
		print("SSH session failed on login.")
		print(str(s))
	else:
		print("SSH session login successful")
		s.sendline ('echo 1 > '+ file)
		s.logout()
