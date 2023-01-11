#!/bin/bash
##
##
## Copyright (c) 2020 Adrian Campazas Vega, Ignacio Samuel Crespo Martinez, Angel Manuel Guerrero Higueras.
##
## This file is part of DOROTHEA 
##
## DOROTHEA is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## DOROTHEA is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##

#We transform the flows stored in the router in a csv
mergecap -w /home/total-traffic/merged.pcap /home/tcpdump-captures/*

cd /home/CICFlowMeter40/bin/
#We generate the CICFlowMEter of each pcap
./cfm /home/tcpdump-captures/  /home/cic-flows/

cat /home/cic-flows/*.csv > /home/cic-total/cic-merged.csv

python3 /clean-CIC.py

#We instruct the receiver to export the captured netflow flows
sshpass -p "password" ssh -o StrictHostKeyChecking=no root@152.148.48.4  "echo 1 > /checkReceiver.txt"
sshpass -p "password" ssh -o StrictHostKeyChecking=no root@152.148.48.3  "echo 1 > /checkNetflow.txt"

#We wait for the receiver to finish
while true;

do

	var=$(cat /checkRouter.txt)
	var2=$(cat /checkRouterNetflow.txt)
	
	if [ $var -eq 2 ] && [ $var2 -eq 2 ];then
    		break;
	else 
		sleep 20
	fi
done
