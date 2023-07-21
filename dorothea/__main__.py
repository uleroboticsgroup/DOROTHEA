import time
import argparse
import sys

from Dorothea import *
from UserActions import *
from utils import enlapsed_time_formater, time_to_refresh


if __name__ == '__main__':

    # Possible values for arguments
    lab_types = ['vanilla', 'hostile']
    nf_versions = ['1', '5', '9', '10', 'psamp']

    parser = argparse.ArgumentParser(description= \
        """
        Docker-based framework for gathering netflow traffic

        """)
    parser.add_argument(
        "-e",
        "--env",
        choices=lab_types,
        help="type of environtment to run, (Default: vanilla)",
        default='vanilla'
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="fail safe clean of docker objects",
        action='store_true'
    )
    parser.add_argument(
        "-v",
        "--version",
        choices=nf_versions,
        help="version to export the netflows as stated in softflowd, (Default: 10 == IPFIX)",
        default='10'
    )
    
    # Parsing argument options
    args = parser.parse_args()

    # Deep cleaning
    # Clean all dorothea docker objects in case there is something left after execution
    if args.clean:
        print("Deep cleaning DOROTHEA\n All DOROTHEA Docker resources removed")
        Dorothea.fail_save_cleaning()
        sys.exit(0)

    try:
        # Start timer
        start_time = time.time()

        # Creatting user actions objects for each env
        vanilla_ua = UserActions('vanilla_actions.yml')
        hostile_ua = UserActions('hostile_actions.yml')

        # Creating dorothea skeleton
        my_dorothea = Dorothea(args.version)

        # Deploying nodes
        if args.env == 'hostile':
            my_dorothea.deploy_hostile(hostile_ua.queue_list)
        #if args.env == 'vanilla':
        my_dorothea.deploy_vanilla(vanilla_ua.queue_list)

        # Giving some time for Rabbit and agents to start up
        length, seconds = 50, 8
        for i in range(length):
            negative = length - i
            print(MAGENTA + f"Starting: [{'#' * i}{'.' * negative}]" + RESET, end='\r')
            time.sleep(seconds/length)

        # Loading tasks into queue
        if args.env == 'hostile':
            hostile_ua.connect(my_dorothea.rabbit_container_ip)
            hostile_ua.load_vanilla_actions()
        #if args.env == 'vanilla':
        vanilla_ua.connect(my_dorothea.rabbit_container_ip)
        vanilla_ua.load_vanilla_actions()
        
      
        # Main loop
        # Prints output every x interval
        while True:
            
            os.system('clear')

            # Printing netflows captured
            for line in my_dorothea.get_captured_flows():
                print(CYAN + line + RESET)

            # Complementary info
            print(YELLOW + "Access rabbitmq-manager at: " + RESET + BOLD + "http://localhost:15672" + RESET)
            print(YELLOW + f"Exit [ Ctrl + C ], elapsed Time: {enlapsed_time_formater(time.time() - start_time)}" + RESET)

            time_to_refresh("Time to refresh", 20)

    # Exit program
    except KeyboardInterrupt as e:
        del my_dorothea
        print(e)
    except Exception as e:
        print(e)
        pass