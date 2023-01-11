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
import paramiko, logging, warnings, random, argparse
from logging.handlers import RotatingFileHandler
from system.printLog import echoC
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
logging.getLogger("paramiko").setLevel(logging.INFO)

sshServer = "140.30.20.9"
sshUser = "root"
sshPassword = "password"
sshCMD = ["uname -r" , "ls", "pwd" ,"ps aux", "whoami" , "df -h" , "ifconfig" , "hostname"]

# Setting up logging
logger = logging.getLogger(__name__)
logLevel = 'DEBUG'
maxSize = 10000000
numFiles = 10
handler = RotatingFileHandler('actor.log',maxBytes=maxSize,backupCount=numFiles)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel("DEBUG")

# Setting up Paramiko Log
paramiko.util.log_to_file("paramiko.log")
echoC("ssh",'*' * 80 + '\n')
echoC("ssh","Did you know we can decrypt SSH?")
echoC("ssh",'*' * 80 + '\n') 

def main(port):
    '''
    This function is a simple SSH connector. The purpose is to generate a live traffic
    connection with a SSH resource.
    '''
    try:
        echoC("ssh",'*' * 80)
        echoC("ssh","Generating App-ID Traffic for SSH on port: %s" % str(port))
        echoC("ssh",'*' * 80 + '\n')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(sshServer,username=sshUser,password=sshPassword,port=port)

        for cmd in sshCMD:
            stdin_, stdout_, stderr_ = ssh.exec_command(cmd)
            echoC("ssh",'*' * 80)
            echoC("ssh","SUCCESS, command sent: %s" % cmd)
            echoC("ssh",'*' * 80 + '\n')
            out = stdout_.readlines()
            out = str(out)
            echoC("ssh",'*' * 80)
            echoC("ssh","Command returned: \n")
            echoC("ssh",out)
            echoC("ssh",'*' * 80 + '\n')
            logger.debug("Ran the command %s" % cmd)
        ssh.close()
    except:
        echoC("ssh","Soemthing went wrong with the run_ssh_connect() function.")
        echoC("ssh","Please check the actor.log for details.")
        #logger.error("There was an error sending the commend, here is the output %s", err)

if __name__ == "__main__":
    for each in sshportlist:
        main(each)
