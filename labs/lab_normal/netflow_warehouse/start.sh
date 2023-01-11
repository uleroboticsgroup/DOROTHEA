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

#We establish that the Gateway is the router and not the host
route add default gw 152.148.48.2

route del default gw 152.148.48.1

service flow-capture start

#Open the port that NetFlow will receive

iptables -A INPUT -p udp --dport 2055 -j ACCEPT 


cron && tail -f /var/log/cron.log &

/etc/init.d/ssh start


/bin/bash

