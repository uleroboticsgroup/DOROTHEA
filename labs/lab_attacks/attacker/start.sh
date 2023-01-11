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

#Establish that the Gateway is the router and not the host, in this way all packets will go through our container that generates netflow
route add default gw 152.148.48.2

route del default gw 152.148.48.1

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

/etc/init.d/ssh start &

#launch the workers who carry out the attacks

celery -A attacks worker --loglevel=info 






