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
from datetime import datetime
from ConfigParser import SafeConfigParser
import time
import sys

# Output of date and time, runtime, calling module, and text passed
# Since the module is passed with path and file transfer, these must be truncated (split)
def echoC(modul, text):

	# An forward and backward Slash splits 
	modulName = modul.split("/")[-1].split("\\")[-1]
	
	# Remove file ending 	
	modulName = modulName.split(".")[-1]

	# Log text: date and time, runtime, module name (field always 11 characters), text passed (without whitespaces)
	outputText = datetime.now().strftime("%y%m%d-%H%M%S") + " | " + "{0:15s}".format(modulName) + " | " + str(text).rstrip()
	#print(outputText)
	
	# Save in Logfile 
	with open("/generate-traffic/system/tracelog.txt", "a") as myFile:
		myFile.write(outputText + "\n")
