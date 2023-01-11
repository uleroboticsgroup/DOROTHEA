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
import browsing.browsing as br
import mailing.mailing as mail
import ssh.sshtraffic as traffic
import meet.botjitmeet as meet
import system.printLog as log
import time
import os

sshportlist = [22,80,443,636,3389]

meet.main()

while 1:
	#We simulate doing internet searches
	br.main('p')
	log.echoC("User", "I take a break")
	time.sleep(20)
	log.echoC("User", "I'm back from the break")
	#os.system("killall firefox 2> /dev/null")
	
	#We simulate a user who sends emails
	mail.main()
	log.echoC("User", "I take a break")
	time.sleep(20)
	log.echoC("User", "I'm back from the break")

	#We simulate connecting to a machine by ssh
	for each in sshportlist:
		traffic.main(each)

		log.echoC("User", "I take a break")
		time.sleep(3)
		log.echoC("User", "I'm back from the break")
