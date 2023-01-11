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


ARG SYSTEM
FROM $SYSTEM

#Install the necessary packages 
RUN apt-get -y update;
RUN apt-get -y install net-tools
RUN apt-get -y install apt-utils
RUN apt-get -y install iputils-ping nano tcpdump
RUN apt-get update && apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN pip3 install pandas

# Enable forwarding
RUN sysctl net.ipv4.conf.all.forwarding=1 

# Install and configure the Netflow sensor
RUN apt-get -y install git
RUN apt-get -y install module-assistant
RUN apt-get -y install build-essential
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get -y install iptables-dev; exit 0
RUN apt-get -y install libxtables-dev iptables-netflow-dkms; exit 0
RUN apt-get -y install iptables libxtables-dev iptables-netflow-dkms pkg-config 
RUN DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get install -y -q --allow-change-held-packages linux-image-$(uname -r)
RUN apt-get -y install linux-headers-$(uname -r)
RUN apt-get -y install cron

#Install mergecap included in Wireshark and libcap since CIC needs this dependency
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wireshark-common
RUN apt-get install -y libpcap-dev

#Clone the project that emulates a router with netflow
#RUN git clone git://github.com/aabc/ipt-netflow.git ipt-netflow;
RUN git clone https://github.com/aabc/ipt-netflow.git ipt-netflow;

#Create the results folder
RUN mkdir /home/netflow_flows

#Launch the proyect
WORKDIR /ipt-netflow
RUN ./configure
RUN make all install
RUN depmod

#Install ssh server
RUN apt-get update && apt-get install -y openssh-server
RUN apt-get install sshpass
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
EXPOSE 22

#Check if the attacks have been carried out and if so we save the results
WORKDIR /



COPY ./netflow_generator/CIC-cron /etc/cron.d/CIC-cron
RUN chmod 0644 /etc/cron.d/CIC-cron
RUN crontab /etc/cron.d/CIC-cron
RUN touch /var/log/cron.log

RUN mkdir /home/tcpdump-capture/
RUN mkdir /home/total-traffic/

RUN echo 0 > checkNetflow.txt
COPY ./netflow_generator/get-data.sh .
RUN chmod +x get-data.sh

#Launch start.sh
COPY ./netflow_generator/start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]

