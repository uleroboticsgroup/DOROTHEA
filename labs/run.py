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
import os
import argparse
import yaml
from joblib import dump, load
import sys
import signal

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", help="attack or normal type")
parser.add_argument("-c", "--clean",nargs='?',const='clean',help="clean all struct")
args = parser.parse_args()
signal.signal(signal.SIGINT, signal.SIG_IGN)

if os.geteuid() != 0:
    print('You must have root privileges for this script.')
    sys.exit(1)

if not args.type:
	print("a type is required")
	parser.print_help()
	quit()


#We read the configuration file
with open("config.yaml") as f:
	conf_file = yaml.load(f, Loader=yaml.FullLoader)
f.close()

if args.clean:

	os.system('docker rm $(docker ps -a -q)')
	os.system('docker rmi $(docker images -q)')
if args.type == 'attack':
	system = os.popen("egrep '^(VERSION_ID|NAME)=' /etc/os-release | awk -F \"=\" '{print $2}' | tr \"\n\" ':' | tr -d '\"\"' | tr [[:upper:]] [[:lower:]] | sed 's/.$//'")

	version = 'SYSTEM:' + str(system.read())

	f = open('./lab_attacks/.env', 'w')
	try:
		#print(version)
		f.write(version)
	finally:
	    f.close()
	#Delete the kernel module
	os.system('sudo rmmod ipt_NETFLOW 2> /dev/null')

	attackers = conf_file["lab_attacks"]["attackers"]
	slaves = conf_file["lab_attacks"]["slaves"]

	# Change slaves.
	os.system('sed -i \'/slaves = /c\\\tslaves = '+ str(slaves) +'\' ./lab_attacks/attacks/tasks.py')
	
	#We change the sampling
	if conf_file["lab_attacks"]["sampling"]["enabled"] == True:
		sampling = conf_file["lab_attacks"]["sampling"]["packet_sampling"]
	else:
		sampling = 1
	os.system('sed -i \'/sampling=/c\\sampling='+str(sampling)+'\' ./lab_attacks/router/start.sh')
	
	#change ips
	with open("lab_attacks/docker-compose.yml") as f:
		conf_file_compose = yaml.load(f, Loader=yaml.FullLoader)
		attacknet_old = conf_file_compose["networks"]["attacknet"]["ipam"]["config"]
		internal_net_old = conf_file_compose["networks"]["internalnet"]["ipam"]["config"]
	f.close()

	internal_new = conf_file["lab_attacks"]["networks"]["internal_net"]
	attacknet_new = conf_file["lab_attacks"]["networks"]["attacker_net"]
	os.system('find ./lab_attacks/ -name "*.*" -print | xargs sed -i "s/' + attacknet_old[0]["gateway"][:-2] +'/'+attacknet_new[:-2]+'/g"')
	os.system('find ./lab_attacks/ -name "*.*" -print | xargs sed -i "s/' + internal_net_old[0]["gateway"][:-2] +'/'+internal_new[:-2]+'/g"')



	os.system('docker-compose -f ./lab_attacks/docker-compose.yml build')
	os.system('docker-compose -f ./lab_attacks/docker-compose.yml up --scale attacker='+str(attackers)+' --scale slave='+str(slaves)+' --force-recreate --abort-on-container-exit')



if args.type == 'normal':
	system = os.popen("egrep '^(VERSION_ID|NAME)=' /etc/os-release | awk -F \"=\" '{print $2}' | tr \"\n\" ':' | tr -d '\"\"' | tr [[:upper:]] [[:lower:]] | sed 's/.$//'")

	version = 'SYSTEM:' + str(system.read())

	f = open('./lab_normal/.env', 'w')
	try:
		#print(version)
		f.write(version)
	finally:
	    f.close()
	os.system('sudo rmmod ipt_NETFLOW 2> /dev/null')

	generators = conf_file["lab_normal"]["generators"]
	if conf_file["lab_normal"]["sampling"]["enabled"] == True:
		sampling = conf_file["lab_normal"]["sampling"]["packet_sampling"]
	else:
		sampling = 1

	#We change the sampling
	os.system('sed -i \'/sampling=/c\\sampling='+str(sampling)+'\' ./lab_normal/router/start.sh')


	#Change mail config

	user = conf_file["lab_normal"]["mailing"]["username"]
	pw = conf_file["lab_normal"]["mailing"]["password"]
	smtp = conf_file["lab_normal"]["mailing"]["smtp"]

	os.system('sed -i \'/user =/c\\user = '+str(user)+'\' ./lab_normal/generator/generate-traffic/mailing/mail.ini')
	os.system('sed -i \'/pw/c\\pw = '+str(pw)+'\' ./lab_normal/generator/generate-traffic/mailing/mail.ini')
	os.system('sed -i \'/smtp/c\\smtp = '+str(smtp)+'\' ./lab_normal/generator/generate-traffic/mailing/mail.ini')


	#change ips
	with open("lab_normal/docker-compose.yml") as f:
		conf_file_compose = yaml.load(f, Loader=yaml.FullLoader)
		internet_old = conf_file_compose["networks"]["internet"]["ipam"]["config"]
		internal_net_old = conf_file_compose["networks"]["internalnet"]["ipam"]["config"]
	f.close()

	internal_new = conf_file["lab_normal"]["networks"]["internal_net"]
	internet_new = conf_file["lab_normal"]["networks"]["internet"]
	os.system('find ./lab_normal/ -name "*.*" -print | xargs sed -i "s/' + internet_old[0]["gateway"][:-2] +'/'+internet_new[:-2]+'/g"')
	os.system('find ./lab_normal/ -name "*.*" -print | xargs sed -i "s/' + internal_net_old[0]["gateway"][:-2] +'/'+internal_new[:-2]+'/g"')
	os.system('docker-compose -f ./lab_normal/docker-compose.yml build')
	os.system('docker-compose -f ./lab_normal/docker-compose.yml up --scale generator='+str(generators)+' --force-recreate -d')

	while True:
		print('Press any key to see the flowNumbers, write save to end the lab')
		fin = input()
		if fin == "save":
			print('Saving data, wait please')
			os.system('docker-compose -f ./lab_normal/docker-compose.yml exec router ./getCIC.sh ')
			os.system('docker-compose -f ./lab_normal/docker-compose.yml down')
			print('data stored, BYE!!!!!')
			break
		else:
			os.system('docker-compose -f ./lab_normal/docker-compose.yml exec netflow_warehouse ./checkFlows.sh')
