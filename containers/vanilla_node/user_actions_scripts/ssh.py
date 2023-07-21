#!/usr/bin/env python3

import paramiko
import time
import sys


for i in range(5):

    time.sleep(60)


    # Create an SSH client instance
    ssh_client = paramiko.SSHClient()

    # Automatically add the server's host key (this is not recommended in a production environment)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SSH server
    hostname = sys.argv[1]
    port = 22  # Default SSH port
    username = "root"
    password = "dorothea"

    ssh_client.connect(hostname, port, username, password)

    iterations = int(sys.argv[2])
    sleep_time = int(sys.argv[3])

    for i in range(iterations):

        # Now you can execute commands or perform other tasks over SSH
        _, stdout, _  = ssh_client.exec_command('echo $(date) @ ${HOSTNAME}')

        print(stdout.read().decode('utf-8').strip())
        time.sleep(sleep_time)

    # Close the SSH connection when done
    ssh_client.close()
