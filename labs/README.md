######## EXECUTE THE LAB #####################

We set up the labs in the **conf.yaml** file. In it we can change the network interfaces, if we want the traffic to be sampled and the credentials to generate email traffic.

* To execute the attacker lab: 


`sudo python3 run.py -t attack`


* To execute the generate normal traffic lab: 

`sudo python3 run.py -t normal`

When we want to stop go generate normal traffic, we write save and automatically the lab **save** the traffic captured and the flows and it close it.


* If we want to clean the entire environment of the lab run: 

`sudo python3 run.py -c`