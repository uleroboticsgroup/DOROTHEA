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
from .tasks import scan_ports
from celery.result import ResultSet
from .end_attack.end_attack import end_attack
import time
import subprocess as sp

r = ResultSet([])

def start_attack():
	NUMBER_OF_PORTS = 65535
	current_port = 1
	scanner_number = 9
	#This number must be a divisor of 65535
	port_range = 771
	#Types of port scans in the nmap tool		
	scanner_type = ['-sU','-sO','-sM','-sN','-sF','-sS','-sT','-sA','-sW','-sX']
	netx_port = port_range
	global r
	while netx_port < NUMBER_OF_PORTS or scanner_number != 0:
		r.add(scan_ports.delay(current_port,netx_port,scanner_type[scanner_number]))
		if netx_port == NUMBER_OF_PORTS:
				scanner_number = scanner_number -1
				current_port = 1
				netx_port = 771

		#Update the ports to scan
		current_port = netx_port
		netx_port = netx_port + port_range
	

def end_attacks():
	global r
	r.join()
	if r.ready() == True:
		end_attack()




if __name__ == '__main__':
	start_attack()
	end_attacks()
