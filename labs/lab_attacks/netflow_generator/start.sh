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


route add default gw 140.30.20.2

route del default gw 140.30.20.1

#Indicate that  machine  will receive the flows
insmod ipt-netflow/ipt_NETFLOW.ko destination=140.30.20.4:2055 debug=1

iptables -P OUTPUT DROP
iptables -P FORWARD DROP

#Rules so that the traffic that reaches the machine is not duplicated

iptables -A INPUT -i eth0 -p tcp --dport 22   -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 22 -d 152.148.48.254 -m state --state ESTABLISHED -j ACCEPT

iptables -A OUTPUT -o eth0 -p tcp --dport 22 -d 152.148.48.254 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

#We redirect the traffic to the netflow module, to generate the flows

iptables -I FORWARD -j NETFLOW
iptables -I INPUT -j NETFLOW
iptables -I OUTPUT -j NETFLOW

#Launch cron to generate CIC flows
cron && tail -f /var/log/cron.log &

/etc/init.d/ssh start

tcpdump -i eth0 -C 1  -w '/home/tcpdump-capture/capture.pcap'

/bin/bash
