######## EXECUTE THE LAB #####################

1  Go to the folder where the docker-compose is located

2  Build:

- Lab with only one attacker: **docker-compose -f docker-compose-simple-attacker.yml build**
    
- Lab with N attackers: **docker-compose build**

3  To start de lab:

- Lab with only one attacker: **docker-compose -f docker-compose-simple-attacker.yml up --scale slave=N --abort-on-container-exit --force-recreate**

- Lab with N attackers: **docker-compose up --scale attacker=N --scale slave=N --abort-on-container-exit --force-recreate**

<br />
<br />
<br />

##########  RUN A NEW ATTACK SCRIPT IN THE LAB WITH ONE ATTACKER ######################


1  Copy you script into **attacker_simple/attacks** folder

2  In the **attacker_simple/start.sh** put the code that execute your script like this:

    python3 attackGenerator.py

3  Build: **docker-compose -f docker-compose-simple-attacker.yml build**

4  Execute: **docker-compose -f docker-compose-simple-attacker.yml up --scale slave=N --abort-on-container-exit --force-recreate**

<br />
<br />
<br />

##########  RUN A NEW ATTACK SCRIPT IN THE LAB WITH N ATTACKER ######################
<br />

1  Define your attack in the **attacks/tasks.py** file like this:

```
def scan_ports(start_port,end_port,scanner_type): 

	nm = nmap.PortScanner()
	results = nm.scan(randomize_ip(), str(start_port) + '-'+ str(end_port), arguments=scanner_type)
	print(results)
```



2 Execute your attack in the function **start_attack()** in the **attacks/run_tasks.py** file.

The attack is a task that will get in a queue and will be executed by the attackers. We must execute the attack as many times as necessary. The following is an example of how to execute the attack:

    
```
def start_attack():
	NUMBER_OF_PORTS = 10000
	current_port = 1
	scanner_number = 7
	port_range = 1000
	scanner_type = ['-sM','-sN','-sF','-sS','-sT','-sA','-sW','-sX']
	netx_port = port_range
	global r
	while netx_port < NUMBER_OF_PORTS or scanner_number != 0:
		r.add(scan_ports.delay(current_port,netx_port,scanner_type[scanner_number]))
		if netx_port == NUMBER_OF_PORTS:
				scanner_number = scanner_number -1
				current_port = 1
				netx_port = 1000

		#We update the ports to scan
		current_port = netx_port
		netx_port = netx_port + port_range
```



3  Build: **docker-compose build**

4  Execute: **docker-compose up --scale attacker=N --scale slave=N --abort-on-container-exit --force-recreate**

