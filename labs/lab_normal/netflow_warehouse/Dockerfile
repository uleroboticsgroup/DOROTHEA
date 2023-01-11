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
FROM ubuntu:18.04

#Install the necessary packages 
RUN apt-get -y update
RUN apt-get -y install apt-utils
RUN apt-get -y install net-tools
RUN apt-get install -y iputils-ping traceroute nano
RUN apt-get install iptables -y 

#Install and configure the Flow-tools tool to save Netflow traffic
RUN apt-get -y install flow-tools
RUN apt-get -y install cron
ADD flow-capture.conf /etc/flow-tools/flow-capture.conf
RUN mkdir /var/log/flow
RUN mkdir /home/netflow_flows



#Install the ssh server
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

#File to check that the receiver has finished
RUN echo 0 > checkReceiver.txt

#Copy the script to generate the flows
COPY getNetflow.sh .
COPY checkFlows.sh .
COPY netflow-cron /etc/cron.d/netflow-cron
RUN chmod 0644 /etc/cron.d/netflow-cron
RUN crontab /etc/cron.d/netflow-cron
RUN touch /var/log/cron.log
RUN chmod +x getNetflow.sh
RUN chmod +x checkFlows.sh


#Launch start.sh
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]



