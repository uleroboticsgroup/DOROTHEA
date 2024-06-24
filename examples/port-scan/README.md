# Port scan

Example to so how to collect the flows during a SSH brute force attack with [DOROTHEA](../../README.md) & [nmap](https://nmap.org/).


## Usage guide

```bash
$ cd examples/port-scan
```

Check the configuration file (dorothea-pmacctd.conf), and the `nmap` arguments on the (docker-compose.yml) `attacker` command.

> The services (containers) will be attached to the default docker network `docker0` with subnet `172.17.0.0/16`.
> Check this values in case you have different ones on your environtment or you created some modifications to this scenario.


### Start lab
```bash
$ docker compose up
```

### Stop lab
```bash
$ docker compose down
```