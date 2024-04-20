import datetime
import logging
import os

import docker


class Dorothea:
    """
    Dorothea singelton class

     Args:
        out_dir (str): output directory for caps, logs and csv
        vanilla_ql (list, optional): list of vanilla worker nodes. Defaults to [].
        hostile_ql (list, optional): list of hostile worker nodes. Defaults to [].
        nf_version (int, optional): softflowd version for exporting the netflows. Defaults to 10.
        sampling (int, optional): sofflowd sampling parameter. Defaults to 1.
        clean (bool, optional): remove container on stop. Defaults to False.

    Returns:
        Dorothea: Unique instance of dorothea
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Dorothea, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(
        self, out_dir, vanilla_ql=[], hostile_ql=[], nf_version=10, sampling=1, clean=True
    ):
        if not hasattr(self, "initialized"):
            self.initialized = True

            self._softflowd_export_version = nf_version
            self._client = docker.from_env()
            self._vanilla_queue_list = vanilla_ql
            self._hostile_queue_list = hostile_ql
            self._output_dir = out_dir
            self._sampling = sampling
            self._clean = clean

    def __enter__(self):
        self.start()
        return self  # The value returned by __enter__ is assigned to the variable after 'as'

    def start(self):
        """
        Start dorothea
        """
        self.build_context_setup()
        logging.info("Starting DOROTHEA.")
        self._set_up_networks()
        self._build_images()
        self._deploy_containers()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def stop(self):
        """
        Stop dorothea
        """
        self.dump_to_csv()
        logging.info("Closing DOROTHEA.")
        self._remove_containers()
        if self._clean:
            self._remove_images()
        self._remove_networks()
        self._client.close()

    def _set_up_networks(self):
        """
        Creates dorothea docker networks
        """
        logging.info("Creating (dorothea_lan) docker network.")
        try:
            self._lan_network = self._client.networks.create(
                "dorothea_lan",
                driver="bridge",
                ipam=docker.types.IPAMConfig(
                    pool_configs=[
                        docker.types.IPAMPool(subnet="10.8.8.0/24", gateway="10.8.8.1")
                    ]
                ),
            )
        except Exception as e:
            logging.error(e)

        logging.info("Creating (dorothea_tools) docker network.")
        try:
            self._tools_network = self._client.networks.create(
                "dorothea_tools",
                driver="bridge",
                ipam=docker.types.IPAMConfig(
                    pool_configs=[
                        docker.types.IPAMPool(subnet="10.8.9.0/24", gateway="10.8.9.1")
                    ]
                ),
            )
        except Exception as e:
            logging.error(e)

    def _remove_networks(self):
        """
        Remove dorothea networks
        """
        logging.info("Removing (dorothea_lan) docker network.")
        try:
            self._lan_network.remove()
        except Exception as e:
            logging.error(e)

        logging.info("Removing (dorothea_tools) docker network.")
        try:
            self._tools_network.remove()
        except Exception as e:
            logging.error(e)

    def _build_images(self):
        """
        Creates dorothea docker images
        """
        logging.info("Building (dorothea/netflow_collector) docker image.")
        try:
            self._collector_image = self._client.images.build(
                path="containers/netflow_collector",
                tag="dorothea/netflow_collector:latest",
                rm=True,
            )
        except Exception as e:
            logging.error(e)

        logging.info("Building (dorothea/netflow_exporter) docker image.")
        try:
            self._exporter_image = self._client.images.build(
                path="containers/netflow_exporter",
                tag="dorothea/netflow_exporter:latest",
                rm=True,
            )
        except Exception as e:
            logging.error(e)

        logging.info("Building (dorothea/vanilla_node) docker image.")
        try:
            self._vanilla_node_image = self._client.images.build(
                path="containers/vanilla_node",
                tag="dorothea/vanilla_node:latest",
                rm=True,
            )
        except Exception as e:
            logging.error(e)

        logging.info("Building (dorothea/hostile_node) docker image.")
        try:
            self._hostile_node_image = self._client.images.build(
                path="containers/hostile_node",
                tag="dorothea/hostile_node:latest",
                rm=True,
            )
        except Exception as e:
            logging.error(e)

    def _remove_images(self):
        """
        Remove dorothea docker images
        """
        logging.info("Removing (dorothea/netflow_collector) docker image.")
        try:
            self._client.images.remove(self._collector_image[0].id)
        except Exception as e:
            logging.error(e)

        logging.info("Removing (dorothea/netflow_exporter) docker image.")
        try:
            self._client.images.remove(self._exporter_image[0].id)
        except Exception as e:
            logging.error(e)

        logging.info("Removing (dorothea/vanilla_node) docker image.")
        try:
            self._client.images.remove(self._vanilla_node_image[0].id)
        except Exception as e:
            logging.error(e)

        logging.info("Removing (dorothea/hostile_node) docker image.")
        try:
            self._client.images.remove(self._hostile_node_image[0].id)
        except Exception as e:
            logging.error(e)

    def _deploy_containers(self):
        """
        Deploys dorothea docker containers
        """
        logging.info("Deploying (dorothea-rabbitmq) docker container.")
        try:
            self._rabbit_container = self._client.containers.run(
                image="rabbitmq:3-management",
                name="dorothea-rabbitmq",
                network=self._lan_network.id,
                detach=True,
                environment={
                    "RABBITMQ_DEFAULT_USER": "dorothea",
                    "RABBITMQ_DEFAULT_PASS": "dorothea",
                },
                hostname="rabbit-queue",
                ports={"15672/tcp": 15672},
            )
        except Exception as e:
            logging.error(e)

        logging.info("Deploying (dorothea-netflow_collector) docker container.")
        try:
            self._collector_container = self._client.containers.run(
                image=self._collector_image[0].id,
                name="dorothea-netflow_collector",
                detach=True,
                network=self._tools_network.id,
                volumes=[
                    f"{os.getcwd()}/{self._output_dir}:/nfcaps",
                ],
            )
        except Exception as e:
            logging.error(e)

        logging.info("Deploying (dorothea-netflow_exporter) docker container.")
        try:
            self._collector_container.reload()
            self._exporter_container = self._client.containers.run(
                image=self._exporter_image[0].id,
                name="dorothea-netflow_exporter",
                environment={
                    "INTERFACE": f"br-{self._lan_network.short_id}",
                    "SERVER_PORT": f"{self._collector_container.attrs['NetworkSettings']['Networks']['dorothea_tools']['IPAddress']}:9555",
                    "NF_VERSION": self._softflowd_export_version,
                    "SAMPLING_RATE": self._sampling,
                },
                detach=True,
                network="host",
            )
        except Exception as e:
            logging.error(e)

        # Worker containers
        self._vanilla_nodes = []
        if self._vanilla_queue_list:
            self._rabbit_container.reload()
            self._rabbit_container_ip = self._rabbit_container.attrs["NetworkSettings"][
                "Networks"
            ]["dorothea_lan"]["IPAddress"]
            for i, queue in enumerate(self._vanilla_queue_list):
                logging.info(f"Deploying (dorothea-node_{i + 1}) docker container.")
                try:
                    node = self._client.containers.run(
                        image=self._vanilla_node_image[0].id,
                        name=f"dorothea-node_{(i + 1)}",
                        environment={
                            "RABBITMQ_HOST": self._rabbit_container_ip,
                            "RABBITMQ_QUEUE": queue,
                        },
                        detach=True,
                        network=self._lan_network.id,
                        hostname=f"node-{(i + 1)}",
                    )
                    self._vanilla_nodes.append(node)
                except Exception as e:
                    logging.error(e)

        self._hostile_nodes = []
        if self._hostile_queue_list:
            self._rabbit_container.reload()
            self._rabbit_container_ip = self._rabbit_container.attrs["NetworkSettings"][
                "Networks"
            ]["dorothea_lan"]["IPAddress"]
            for i, queue in enumerate(self._hostile_queue_list):
                logging.info(f"Deploying (dorothea-hostile_{i + 1}) docker container.")
                try:
                    node = self._client.containers.run(
                        image=self._hostile_node_image[0].id,
                        name=f"dorothea-hostile_{(i + 1)}",
                        environment={
                            "RABBITMQ_HOST": self._rabbit_container_ip,
                            "RABBITMQ_QUEUE": queue,
                        },
                        detach=True,
                        network=self._lan_network.id,
                        hostname=f"hostile-{(i + 1)}",
                    )
                    self._hostile_nodes.append(node)
                except Exception as e:
                    logging.error(e)

    def _remove_containers(self):
        """
        Remove dorothea docker containers
        """
        logging.info(f"Removing (dorothea-rabbitmq) docker container.")
        self._rabbit_container.remove(force=True, v=True)
        logging.info(f"Removing (dorothea-netflow_collector) docker container.")
        self._collector_container.remove(force=True, v=True)
        logging.info(f"Removing (dorothea-netflow_exporter) docker container.")
        self._exporter_container.remove(force=True, v=True)

        if self._vanilla_nodes:
            for node in self._vanilla_nodes:
                logging.info(f"Removing ({ node.name }) docker container.")
                node.remove(force=True, v=True)

        if self._hostile_nodes:
            for node in self._hostile_nodes:
                logging.info(f"Removing ({ node.name }) docker container.")
                node.remove(force=True, v=True)

    def get_rabbitmq_host(self):
        """
        Get the IP of Rabbit-MQ container
        """
        self._rabbit_container.reload()
        return self._rabbit_container.attrs["NetworkSettings"]["Networks"][
            "dorothea_lan"
        ]["IPAddress"]

    def get_captured_flows(self):
        """
        Simple dump of flows captured in collector with out the Rabbit-MQ iteractions.
        """
        command = [
            "nfdump",
            "-R",
            "/nfcaps/caps",
            "-O",
            "tstart",
            f"not src ip {self._rabbit_container_ip} and not dst ip {self._rabbit_container_ip}",
        ]
        exit_code, output = self._collector_container.exec_run(command)
        return output.decode("utf-8").split("\n")

    def dump_to_csv(self):
        """
        Dumps the dataflows collected by the collector node in a CSV.
        """
        logging.info(f"Saving flows to CSV at {self._output_dir}/flows.csv")
        try:
            command = [
                "nfdump",
                "-R",
                "/nfcaps/caps",
                "-O",
                "tstart",
                "-o",
                "csv",
                f"not src ip {self._rabbit_container_ip} and not dst ip {self._rabbit_container_ip}",
            ]
            exit_code, output = self._collector_container.exec_run(command)

            with open(self._output_dir + "/flows.csv", "wb") as flows_f:
                flows_f.write(output)
        except Exception as e:
            logging.error(e)

    @staticmethod
    def build_context_setup(path="containers"):
        """
        Class method to copy cummon node resources to each node build context.

        Args:
            path(str): Path to the 'containers' directory
        """

        logging.info("Generating (dorothea_daemon.py) for node containers.")
        containers_content = os.listdir(path)

        node_resources = []
        node_contexts = []
        new_comment = """
            ---DOROTHEA MANAGE COMMENT, DO NOT MODIFY---
            This file gets created on DOROTHEA start up, the changes made in here will not persist next run.
            To modify this file use the file with same name under containers/<file_name>
            """

        for file in containers_content:
            if file.find("_node") != -1:
                node_contexts.append(file)
            elif file.find("node_") != -1:
                node_resources.append(file)

        for file in node_resources:
            content = []
            in_docstring = False
            in_comment = False
            inject_comment = True

            with open(path + "/" + file, "r") as f:
                for line in f:
                    if line == "# [START]\n":
                        in_comment = True
                        content.append(line)
                    elif line == "# [FINISH]\n":
                        in_comment = False
                    elif line == '"""\n':
                        in_docstring = not in_docstring
                    if in_docstring and in_comment:
                        if inject_comment:
                            for l in new_comment.strip().split("\n"):
                                content.append(l.strip() + "\n")
                            inject_comment = False
                    else:
                        content.append(line)

            for context in node_contexts:
                with open(path + "/" + context + "/" + file, "w") as f:
                    for line in content:
                        f.write(line)

    
    def collector_ready(self):
        """
        Check if the collector node "softflowd" is ready to start monitoring.
        """
        command = [
            "ls",
            "/var/run/softflowd.ctl",
        ]
        exit_code, output = self._exporter_container.exec_run(command)
        return exit_code