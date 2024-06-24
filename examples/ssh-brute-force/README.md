# SSH brute force

Example to so how to collect the flows during a SSH brute force attack with [DOROTHEA](../../README.md) & [hydra](https://github.com/vanhauser-thc/thc-hydra).


## Usage guide

First create the resources specified in the compose file with out starting the container with the following command:
```bash
$ docker compose up --no-start
```
This step is needed for docker compose to create the network interface that we will use to listen on.
The interface will be named in the form `br-5d02e59b9a78`, we will need to find the newly created adapter and substitude it on (dorothea-pmacctd.conf) under the field (**cap_interface:**)

> This docker virtual network is needed since the default bridge adapter **docker0** does not support domain name resolution.
> Or own created docker virtual network will support it allowing us to address the containers by the hostnames.

### Find network interface name

```bash
$ ip a
```
If you are not sure which one is the right network interface, you can make user of the command:
```bash
$ docker network ls
```

## Start lab
```bash
$ docker compose up
```

## Stop lab
```bash
$ docker compose down
```