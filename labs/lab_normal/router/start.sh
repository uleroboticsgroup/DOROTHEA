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
sampling=10000
iptables -t mangle -A PREROUTING -m statistic --mode nth --every $sampling --packet 0  -j TEE --gateway 152.148.48.3

#We indicate the default gateway is that of the WAN network, through which it goes to the internet
route add default gw 140.30.20.1
route del default gw 152.148.48.1

#We indicate that NAT traffic goes to the Internet
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE

/etc/init.d/ssh start

#We launch tcp-dump storing the packages every 20 mb
tcpdump -i eth0 -C 1  -w '/home/tcpdump-captures/capture.pcap' 




