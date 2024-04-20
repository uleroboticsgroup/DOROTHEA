import argparse
import datetime
import logging
import os
import sys
import time
from threading import Thread

import click
import docker
import yaml
from halo import Halo

from .dorothea import Dorothea
from .dorothea_pretty import DorotheaPretty
from .rabbitloader import RabbitLoader


def fail_save_cleaning():
    """
    Removes all Dorothea components from Docker.
    In case the script got stuck or exited incorrectly,
    run this method for clean up.
    """
    client = docker.from_env()

    for container in client.containers.list():
        if container.name.find("dorothea") != -1:
            container.remove(force=True, v=True)

    for image in client.images.list():
        if image.tags and image.tags[0].find("dorothea") != -1:
            client.images.remove(image.id, force=True)

    for network in client.networks.list():
        if network.name.find("dorothea") != -1:
            network.remove()


def create_output_dir():
    """
    Creates directory for storing nfcaps in case does not exist
    """
    # Get the current local time
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y.%m.%d_%H-%M-%S")
    # Specify the directory path
    directory_path = f"dump/{formatted_time}"
    # Check if the directory exists
    if not os.path.exists(directory_path + "/caps"):
        # Create the directory
        os.makedirs(directory_path + "/caps")
    return directory_path


def enlapsed_time_formater(elapsed_time_seconds):
    """
    Format a time stamp to H:M:S format

    Args:
        elapsed_time_seconds(float): Timestamp

    Returns:
        (str): String with formated time
    """
    hours = int(elapsed_time_seconds // 3600)
    minutes = int((elapsed_time_seconds % 3600) // 60)
    seconds = int(elapsed_time_seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def load_tasks(rabbit_ip, tasks):
    """
    Parses the YAML files and loads the tasks into the designed queues

    Args:
        rabbit_ip (str): IP of rabbit's container
        tasks (str): string derived from the option --env
    """
    time.sleep(8)
    
    # Creatting rabbitloader objects for each env
    vanilla_ua = RabbitLoader("vanilla_actions.yml")
    hostile_ua = RabbitLoader("hostile_actions.yml")
    
    # Loading vanilla tasks
    vanilla_ua.connect(rabbit_ip)
    vanilla_ua.load_vanilla_actions()

    # Loading hostile tasks
    if tasks == 'hostile':
        hostile_ua.connect(rabbit_ip)
        hostile_ua.load_vanilla_actions()



if __name__ == "__main__":
    # Possible values for arguments
    lab_types = ["vanilla", "hostile"]
    nf_versions = ["1", "5", "9", "10", "psamp"]

    parser = argparse.ArgumentParser(
        description="""
        Docker-based framework for gathering netflow traffic

        """
    )
    parser.add_argument(
        "-c", "--clean", help="fail safe clean of docker objects", action="store_true"
    )
    parser.add_argument(
        "-d", "--dry", help="run dorothea without woker nodes", action="store_true"
    )
    parser.add_argument(
        "-e",
        "--env",
        choices=lab_types,
        help="type of environtment to run, (default: vanilla)",
        default="vanilla",
    )
    parser.add_argument("-r", "--rm-containers", help="remove containers after exiting", action="store_true")
    parser.add_argument("-s", "--sampling", help="samplig rate use by softflowd, (default: 1)", default="1")
    parser.add_argument(
        "-v",
        "--version",
        choices=nf_versions,
        help="version to export the netflows as stated in softflowd, (default: 10 == IPFIX)",
        default="10",
    )

    # Parsing argument options
    args = parser.parse_args()

    # Deep cleaning
    # Clean all dorothea docker objects in case there is something left after execution
    if args.clean:
        h = Halo("Cleaning Dorothea docker resources")
        h.start()
        fail_save_cleaning()
        h.succeed("Dorothea docker resources cleaned")
        sys.exit(0)

    output_dir = create_output_dir()
    
    # Configure the logging module
    logging.basicConfig(
        level=logging.INFO,  # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(output_dir + "/dorothea.log"),  # Log to dump/<date>/dorothea.log
            # logging.StreamHandler(),  # Log to the console
        ],
    )

    # Getting list of worker nodes to build
    vanilla_actions_list = "vanilla_actions.yml"
    hostile_actions_list = "hostile_actions.yml"
    vanilla_queue_list = None
    hostile_queue_list = None

    # Vanilla workers
    with open(vanilla_actions_list, "r") as actions_list:
        yml = yaml.safe_load(actions_list)
        vanilla_queue_list= tuple(
            f"node-{(i + 1)}_{yml['lab']}_v{yml['version']}"
            for i in range(yml["nodes"])
        )
    
    # Hostile workers
    with open(hostile_actions_list, "r") as actions_list:
        yml = yaml.safe_load(actions_list)
        hostile_queue_list= tuple(
            f"node-{(i + 1)}_{yml['lab']}_v{yml['version']}"
            for i in range(yml["nodes"])
        )

    print(args._get_args.__str__())
    dorthea_options = {
        'out_dir': output_dir,
        'vanilla_ql': vanilla_queue_list,
        'hostile_ql': hostile_queue_list if args.env == 'hostile' else [],
        'nf_version': args.version,
        'sampling': args.sampling,
        'clean': args.rm_containers
    }
    
    with DorotheaPretty(**dorthea_options) as drtha:
        start_time = time.time()
        
        h = Halo("Wating for collector to be ready")
        h.start()
        while 0 != drtha.collector_ready():
            time.sleep(1)
        h.succeed("Collector ready")

        # Run the rabbitloader in a separate thread
        rabbit_ip = drtha.get_rabbitmq_host()
        loading_thread = Thread(target=load_tasks, args=(rabbit_ip,args.env))
        loading_thread.start()

        try:
            while True:
                os.system("clear")

                # Printing netflows captured
                for line in drtha.get_captured_flows():
                    print(line)

                # Complementary info
                print("Access rabbitmq-manager at: " + "http://localhost:15672")
                print(
                    f"Press [ Ctrl + C ] for exit, elapsed Time: {enlapsed_time_formater(time.time() - start_time)}"
                )

                with click.progressbar(range(10 * 10), label="Refresh") as bar:
                    for item in bar:
                        # Do time till next refresh
                        time.sleep(0.1)
                        
        except KeyboardInterrupt:
            print()
            h = Halo("Exiting tasks thread")
            h.start()
            loading_thread.join()
            h.succeed("Thread terminated")
