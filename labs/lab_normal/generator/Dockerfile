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
RUN apt-get update 
RUN apt-get install -y net-tools
RUN apt-get update && apt-get install -y iputils-ping traceroute nano wget

#We install the dependencies to execute the project
RUN apt-get install -y openssh-client
RUN apt-get update && apt-get install -y firefox
RUN apt-get install -y psmisc
RUN apt-get update && apt-get install -y python-pip
RUN apt-get -y install cron
COPY netflow-cron /etc/cron.d/netflow-cron
RUN chmod 0644 /etc/cron.d/netflow-cron
RUN crontab /etc/cron.d/netflow-cron
RUN touch /var/log/cron.log
RUN pip install paramiko selenium xvfbwrapper
RUN apt-get install -y xvfb
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -xzvf geckodriver-v0.26.0-linux64.tar.gz
RUN mv geckodriver /opt/
RUN mkdir generate-traffic
COPY generate-traffic/ ./generate-traffic/
RUN chmod +x ./generate-traffic/start_generate_traffic.sh

#Launch start.sh
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
