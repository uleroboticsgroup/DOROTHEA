#!/usr/bin/env python

"""
# [START]
---DOROTHEA MANAGE COMMENT, DO NOT MODIFY---
This file will be copied to the build context of each node image durring DOROTHEA start-up.

# [FINISH]

Script responsible of executting the jobs programed to be run in a desired node and structure its ouputs.
"""

import pika
import sys
import os
import subprocess
import time
import logging
import threading
import multiprocessing
import signal

# ANSI escape codes for colors
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"


class ProcessController:

    connection = None
    channel = None
    credentials = None
    detached_proceses = []

    @classmethod
    def main_loop(cls, rabbitmq_host, queue):

        thread = threading.Thread(target=ProcessController.check_on_detached)

        # Start the thread
        thread.start()

        while True:

            try:
                ProcessController.credentials = pika.PlainCredentials('dorothea', 'dorothea')
                ProcessController.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, credentials= ProcessController.credentials))
                ProcessController.channel = ProcessController.connection.channel()

                #channel.queue_declare(queue='vanilla_actions')

                ProcessController.channel.basic_qos(prefetch_count=1)
                ProcessController.channel.basic_consume(queue= queue, on_message_callback=ProcessController.callback, auto_ack=True)

                logging.info(CYAN + BOLD + ' [*] Waiting for messages. To exit press CTRL+C' + RESET)


                ProcessController.channel.start_consuming()
                ProcessController.cleaning()

            except pika.exceptions.ConnectionClosedByBroker:
                # Uncomment this to make the example not attempt recovery
                # from server-initiated connection closure, including
                # when the node is stopped cleanly
                #
                # break
                continue
            # Do not recover on channel errors
            except pika.exceptions.AMQPChannelError as err:
                print(f"Rabbit-MQ server not running, connection fail.")
            # Recover on all other connection errors
            except pika.exceptions.AMQPConnectionError:
                print("Connection was closed, retrying...")
                continue

    @classmethod
    def stop(cls):
        try:
            ProcessController.channel.stop_consuming()
        except Exception:
            pass

        try:
            ProcessController.connection.close()
        except Exception:
            pass

    @classmethod
    def callback(cls, ch, method, properties, body):

        #body_dict = parsed_dict = yaml.safe_load(body)
        logging.info(GREEN + BOLD + f" [x] Received: [{properties.headers['name']}]" + RESET)
        logging.info(YELLOW + f" [H] Headers: {properties.headers}" + RESET)

        if properties.headers['daemonized']:
            ProcessController.run_detached_process(body)
        else:
            ProcessController.run_process(body)

    @classmethod
    def run_detached_process(cls, command):
        try:
            detached_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ProcessController.detached_proceses.append(detached_process)
            logging.info(BLUE + " " * 3 + f"Detached process started with PID {detached_process.pid}.\n" + RESET)
        except Exception as e:
            logging.info(RED + " " * 3 + f"Error starting detached process: {e}" + RESET)

    @classmethod
    def run_process(cls, command):

        # Run the command and capture its output
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the output and error messages
        logging.info(BLUE + " " * 3 + "Output:" + RESET)
        for line in result.stdout.split("\n"):
            logging.info(" " * 5 + f"{line}")

        logging.info(RED + " " * 3 + "Error:" + RESET)
        for line in result.stderr.split("\n"):
            logging.info(" " * 5 + f"{line}")

        # Print the return code
        logging.info(MAGENTA + " " * 3 + "Return Code: " + RESET + str(result.returncode) + "\n")

    @classmethod
    def check_on_detached(cls):

        while True:
            for i, p in enumerate(ProcessController.detached_proceses):
                
                return_code = p.poll()
                if return_code is not None:
                    p.terminate()
                    stdout, stderr = p.communicate()
                    exitcode = p.returncode

                    logging.info(GREEN + BOLD + f" [x] Finished: PID ({p.pid})" + RESET)

                    # Print the output and error messages
                    logging.info(BLUE + " " * 3 + "Output:" + RESET)
                    for line in stdout.decode('utf-8').split("\n"):
                        logging.info(" " * 5 + f"{line}")

                    logging.info(RED + " " * 3 + "Error:" + RESET)
                    for line in stderr.decode('utf-8').split("\n"):
                        logging.info(" " * 5 + f"{line}")

                    # Print the return code
                    logging.info(MAGENTA + " " * 3 + "Return Code: " + RESET + str(exitcode) + "\n")

                    del ProcessController.detached_proceses[i]



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    rabbitmq_host, queue = sys.argv[1:3]
    logging.info(GREEN + BOLD + f"[ ] Rabbit-MQ server to connect: {rabbitmq_host}" + RESET)
    
    try:
        ProcessController.main_loop(rabbitmq_host, queue) 
    except KeyboardInterrupt:
        ProcessController.stop()
        logging.info(RED + BOLD + "[ ] Exiting daemon" + RESET)
