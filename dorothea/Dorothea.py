import datetime
import docker
import os

from Colors import *
from utils import loading_decorator



# Adding info/progress printouts to some docker methods
docker.models.images.ImageCollection.build = loading_decorator(docker.models.images.ImageCollection.build, "Image build:", "\tBuilding:")
docker.models.containers.ContainerCollection.run = loading_decorator(docker.models.containers.ContainerCollection.run, "Container deployes:", "\tDeploying:")
docker.models.networks.NetworkCollection.create = loading_decorator(docker.models.networks.NetworkCollection.create, "Network created:", "\tCreating:")


class Dorothea:
    """
    Class for creating DOROTHEA lab.

    This class creattes creates the DOROTHEA lab on top of Docker engienne. 

    Attributes:
        client: Docker client found on host
        lan_network: Main DOROTHEA network
        tools_network: Secondary DOROTHEA network
        collector_image: Image with "nfcapd"
        exporter_image: Image with "softflowd
        vanilla_node_image: Image to simulate user actions
        collector_container: Container out of collector_image
        exporter_container: Container out of exporter_image
        vanilla_node_container: Container out of vanilla_node_image
        rabbitmq_container: Container out of rabbitmq:3-management image

    Methods:
        greet_rabbitmq_host(): Return the IP of the Rabbit-MQ container.
        get_captured_flows(): Return the "nfdump" of the collected ncaps.
    """
    def __init__(self, nf_version = 10):
        """
        Creates networks, builds images and deploys containers of lab.

        Args:
            None
        """
        # Bootstraping Images building context
        print(GREEN + f"[ ] Bootstraping build context" + RESET)
        Dorothea._build_context_setup()

        # Docker client
        self.client = docker.from_env()

        # Networks
        print(GREEN + f"[ ] Creating docker networks" + RESET)

        self.lan_network = self.client.networks.create(
            'dorothea_lan', 
            driver= 'bridge', 
            ipam= docker.types.IPAMConfig(
                pool_configs=[docker.types.IPAMPool(
                    subnet='10.8.8.0/24',
                    gateway='10.8.8.1'
                    )
                ]
            )
        )

        self.tools_network = self.client.networks.create(
            'dorothea_tools', 
            driver= 'bridge', 
            ipam= docker.types.IPAMConfig(
                pool_configs=[docker.types.IPAMPool(
                    subnet='10.8.9.0/24',
                    gateway='10.8.9.1'
                    )
                ]
            )
        )

        # Deploying Rabbit-MQ container
        # Started here gives it time to get up and running 
        print(GREEN + f"[ ] Pulling and running Rabbit-MQ" + RESET)

        self.rabbit_container = self.client.containers.run(
            image= 'rabbitmq:3-management',
            name= 'dorothea-rabbitmq',
            network= self.lan_network.id,
            detach= True,
            environment= {
                'RABBITMQ_DEFAULT_USER': 'dorothea',
                'RABBITMQ_DEFAULT_PASS': 'dorothea'
            },
            hostname= 'rabbit-queue',
            ports= {'15672/tcp': 15672}
        )

        # Docker Images
        print(GREEN + f"[ ] Building docker images" + RESET)

        self.collector_image = self.client.images.build(
            path= 'containers/netflow_collector',
            tag= 'dorothea/netflow_collector:latest',
            rm= True
        )
        
        self.exporter_image = self.client.images.build(
            path= 'containers/netflow_exporter',
            tag= 'dorothea/netflow_exporter:latest',
            rm= True
        )
        
        self.vanilla_node_image = self.client.images.build(
            path= 'containers/vanilla_node',
            tag= 'dorothea/vanilla_node:latest',
            rm= True
        )

        self.hostile_node_image = self.client.images.build(
            path= 'containers/hostile_node',
            tag= 'dorothea/hostile_node:latest',
            rm= True
        )

        # Docker Containers
        print(GREEN + f"[ ] Deploying containers" + RESET)

        self._create_output_dir()
        
        self.collector_container = self.client.containers.run(
            image= self.collector_image[0].id,
            name= 'dorothea-netflow_collector',
            detach= True,
            network= self.tools_network.id,
            volumes= [f'{os.getcwd()}/{self._output_dir}/:/nfcaps',]
        )

        self.collector_container.reload()
        self.exporter_container = self.client.containers.run(
            image= self.exporter_image[0].id,
            name= 'dorothea-netflow_exporter',
            environment= {
                'INTERFACE': f'br-{self.lan_network.short_id}',
                'SERVER_PORT': f"{self.collector_container.attrs['NetworkSettings']['Networks']['dorothea_tools']['IPAddress']}:9555",
                'NF_VERSION': nf_version,
            },
            detach= True,
            network= 'host'
        )

    def deploy_vanilla(self, queue_list):
        """
        Deploys the nodes to emulate ordinary user actions

        Args:
            queue_list([str]): List of strings with queues for each node
        """

        self.rabbit_container.reload()
        self.rabbit_container_ip = self.rabbit_container.attrs['NetworkSettings']['Networks']['dorothea_lan']['IPAddress']
        self.nodes = []
        for i, queue in enumerate(queue_list):
            node = self.client.containers.run(
                image= self.vanilla_node_image[0].id,
                name= f'dorothea-node_{(i + 1)}',
                environment= {
                    'RABBITMQ_HOST': self.rabbit_container_ip,
                    'RABBITMQ_QUEUE': queue
                },
                detach= True,
                network= self.lan_network.id,
                hostname= f'node-{(i + 1)}'
            )
            self.nodes.append(node)

    def deploy_hostile(self, queue_list):
        """
        Deploys the hostile nodes to emulate attackers actions

        Args:
            queue_list([str]): List of strings with queues for each node
        """
        self.rabbit_container.reload()
        self.rabbit_container_ip = self.rabbit_container.attrs['NetworkSettings']['Networks']['dorothea_lan']['IPAddress']
        self.hostile_nodes = []
        for i, queue in enumerate(queue_list):
            node = self.client.containers.run(
                image= self.hostile_node_image[0].id,
                name= f'dorothea-hostile_{(i + 1)}',
                environment= {
                    'RABBITMQ_HOST': self.rabbit_container_ip,
                    'RABBITMQ_QUEUE': queue
                },
                detach= True,
                network= self.lan_network.id,
                hostname= f'hostile-{(i + 1)}'
            )
            self.hostile_nodes.append(node)


    @classmethod
    def _build_context_setup(cls, path='containers'):
        """
        Class method to copy cummon node resources to each node build context.

        Args:
            path(str): Path to the 'containers' directory
        """
        containers_content = os.listdir(path)

        node_resources = []
        node_contexts = []
        new_comment = \
            """
            ---DOROTHEA MANAGE COMMENT, DO NOT MODIFY---
            This file gets created on DOROTHEA start up, the changes made in here will not persist next run.
            To modify this file use the file with same name under containers/<file_name>
            """

        for file in containers_content:
            if file.find('_node') != -1:
                node_contexts.append(file)
            elif file.find('node_') != -1:
                node_resources.append(file)


        for file in node_resources:
        
            content = []
            in_docstring = False
            in_comment = False
            inject_comment = True

            with open( path + '/' + file, 'r') as f:
                for line in f:
                    if line == '# [START]\n':
                        in_comment = True
                        content.append(line)
                    elif line == '# [FINISH]\n':
                        in_comment = False
                    elif line == '"""\n':
                        in_docstring = not in_docstring
                    if in_docstring and in_comment:
                        if inject_comment:
                            for l in new_comment.strip().split('\n'):
                                content.append(l.strip() + '\n')
                            inject_comment = False
                    else:
                        content.append(line)

            for context in node_contexts:
                with open(path + '/' + context + '/' + file, 'w') as f:
                    for line in content:
                        f.write(line)


    
    def __del__(self):
        """
        Saving flows as CSV and cleanning DOROTHEA lab

        Args:
            None
        """

        print(RED + '\n[*] Closing DOROTHEA' + RESET)

        # Dump flows to CSV
        try:
            command = ["nfdump", "-R", "/nfcaps", "-O", "tstart", "-o", "csv", f"not src ip {self.rabbit_container_ip} and not dst ip {self.rabbit_container_ip}"]
            exit_code, output = self.collector_container.exec_run(command)

            with open(self._output_dir + '/flows.csv', 'wb') as flows_f:
                flows_f.write(output)
            
            if exit_code == 0:
                print(GREEN + f"[>] Flows dump copleted at [{self._output_dir}/flows.csv]" + RESET)
            else:
                print(RED + "[F] Flows dump failed" + RESET)
        except Exception as e:
            pass


        print(RED + '[ ] Removing containers' + RESET)
        # Containers
        try:
            self.rabbit_container.remove(force=True, v=True)
        except:
            pass
        try:
            self.collector_container.remove(force=True, v=True)
        except:
            pass
        try:
            self.exporter_container.remove(force=True, v=True)
        except:
            pass
        try:
            for node in self.nodes:
                node.remove(force= True, v=True)
        except Exception as e:
            pass

        try:
            for node in self.hostile_nodes:
                node.remove(force= True, v=True)
        except Exception as e:
            pass


        print(RED + '[ ] Removing images' + RESET)
        # Images
        try:
            self.client.images.remove(self.collector_image[0].id)
            self.client.images.remove(self.exporter_image[0].id)
            self.client.images.remove(self.vanilla_node_image[0].id)
        except Exception as e:
            pass


        print(RED + '[ ] Removing networks' + RESET)
        # Networks
        try:
            self.lan_network.remove()
            self.tools_network.remove()
        except Exception as e:
            pass

    def get_rabbitmq_host(self):
        """
        Get the IP of Rabbit-MQ container
        """
        self.rabbit_container.reload()
        return self.rabbit_container.attrs['NetworkSettings']['Networks']['dorothea_lan']['IPAddress']


    def get_captured_flows(self):
        """
        Simple dump of flows captured in collector with out the Rabbit-MQ iteractions.
        """
        command = ["nfdump", "-R", "/nfcaps", "-O", "tstart", f"not src ip {self.rabbit_container_ip} and not dst ip {self.rabbit_container_ip}"]
        result = self.collector_container.exec_run(command)
        return result[1].decode('utf-8').split('\n')
    

    def _create_output_dir(self):
        """
        Creates directory for storing nfcaps in case does not exist
        """
        # Get the current local time
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        # Specify the directory path
        directory_path = f'nfcaps/{formatted_time}_nfcaps'
        # Check if the directory exists
        if not os.path.exists(directory_path):
            # Create the directory
            os.makedirs(directory_path)
        self._output_dir =  directory_path

    @classmethod
    def fail_save_cleaning(cls):
        """
        Removes all Dorothea components from Docker.
        In case the script got stuck or exited incorrectly, 
        run this method for clean up.
        """
        client = docker.from_env()

        for container in client.containers.list():
            if container.name.find('dorothea') != -1:
                container.remove(force=True, v=True)

        for image in client.images.list():
            if image.tags and image.tags[0].find('dorothea') != -1:
                client.images.remove(image.id)

        for network in client.networks.list():
            if network.name.find('dorothea') != -1:
                network.remove()