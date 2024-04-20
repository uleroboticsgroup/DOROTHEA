import logging

import pika
import yaml


class RabbitLoader:
    """
    Class for emulating user actions.

    This class parses the YAML containing the user actions,
    and adds them to a queue on Rabbit-MQ

    Attributes:
        actions_list(str): File containing list of actions
        rabbitmq_host(str): IP container Rabbit-MQ
        queue(str): Name of queue
        connection: Connection to Queue
        channel: Chanel used for connection


    Methods:
        __init__(): Constructs the queues for Rabbit
        load_vanilla_actions(): Parse and push to queue
        connect(): Connects to Rabbit server
    """

    def __init__(self, actions_list) -> None:
        """
        Stablish connection with the Rabbit-MQ server.

        Args:
            host: IP for the Rabbit-MQ server
            actions_list: YAML file with the user actoins.
            queue: Name of queue in Rabbit

        Return:
            None

        """
        logging.basicConfig.level = logging.CRITICAL

        self.actions_list = actions_list

        with open(self.actions_list, "r") as actions_list:
            yml = yaml.safe_load(actions_list)
        self.yml_actions = yml

        self.queue_list = tuple(
            f"node-{(i + 1)}_{yml['lab']}_v{yml['version']}"
            for i in range(yml["nodes"])
        )

        for action in yml["actions"]:
            if action["node"] > yml["nodes"]:
                raise Exception(
                    f"Node {action['node']} out of range in task: {action['name']}"
                )

    def connect(self, host):
        """
        Connects to Rabbit-MQ server/container

        Args:
            host(str): IP of Rabbit-MQ

        Returns:
            None
        """
        self.rabbitmq_host = host
        self.credentials = pika.PlainCredentials("dorothea", "dorothea")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbitmq_host, credentials=self.credentials
            )
        )
        self.channel = self.connection.channel()

        for queue in self.queue_list:
            self.channel.queue_declare(queue=queue)

    def load_vanilla_actions(self):
        """
        Load usual user interatoins

        Parse file containing user actions and push them to the its Rabbit-MQ queue

        Args:
            None

        Return:
            None
        """
        if self.yml_actions["version"] == 1.0:
            for action in self.yml_actions["actions"]:
                queue = self.queue_list[(action["node"] - 1)]

                self.channel.basic_publish(
                    exchange="",
                    routing_key=queue,
                    body=action.pop("payload"),
                    properties=pika.BasicProperties(headers=action),
                )

        else:
            raise Exception("Queue version not suported")

        self.connection.close()
