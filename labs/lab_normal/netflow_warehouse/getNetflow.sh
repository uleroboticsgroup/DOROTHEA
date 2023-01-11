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

var=$(cat /checkReceiver.txt)

if [ $var -eq 1 ]; then
    #We transform the flows stored in the router into a single csv

    sleep 120
    flow-cat /var/log/flow/* | flow-export -f2 > /home/netflow_flows/netflow_flows.csv

    #We tell the router that it's done
    sshpass -p "password" ssh -o StrictHostKeyChecking=no root@152.148.48.2  "echo 2 > /checkRouter.txt"

fi
