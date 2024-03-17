"""Encapsulates the connection information for MQTT,
and provides a method to retrieve the secrets."""
from dataclasses import dataclass
import os
import os.path
import getpass
import json
import random
import ssl

from paho.mqtt import client as mqtt_client


@dataclass
class ConnectionInfo:
    """
    Represents the connection information for MQTT.
    Read up on dataclasses here: https://docs.python.org/3/library/dataclasses.html

    Attributes:
        broker (str): The MQTT broker address.
        port (int): The port number for the MQTT broker.
        user_name (str, optional): The username for authentication (default: None).
        password (str, optional): The password for authentication (default: None).
        topic (str, optional): The MQTT topic to subscribe to (default: None).
    """

    broker: str
    port: int
    user_name: str = None
    password: str = None
    topic: str = None

    def update(self, info: dict) -> None:
        """
        Updates the attributes of the object based on the provided dictionary.

        Args:
            info (dict): A dictionary containing the attribute names as keys
            and their new values as values.
            Accepted keys: 'broker', 'port', 'user_name', 'password', 'topic'.

        Returns:
            None
        """
        for key, value in info.items():
            if hasattr(self, key):
                setattr(self, key, value)


def get_secrets(conn_info: ConnectionInfo, root_file: str = __file__) -> ConnectionInfo:
    """
    Retrieves the MQTT connection secrets from a secrets file or prompts the user to enter them.

    Args:
        conn_info (ConnectionInfo): An instance of the ConnectionInfo class
        that holds the connection information.
        root_file (str, optional): The path to the Python file that calls this function.

    Returns:
        ConnectionInfo: The updated connection_info object with the retrieved or entered secrets.
    """

    # get the path to this Python file
    root_dir = os.path.abspath(os.path.dirname(root_file))
    # get the name of this Python file without the .py extension
    this_file = os.path.basename(root_file)[:-3]
    # create the path to the secrets file, one level up from this file
    secrets_file = os.path.join(
        root_dir, f"../../secrets/{this_file}_secrets.json")

    # load secrets from file if it exists
    if os.path.exists(secrets_file):
        with open(secrets_file, 'r', encoding='utf8') as f:
            conn_info.update(json.load(f))
    else:
        # otherwise ask for them
        if not conn_info.broker:
            conn_info.broker = input("Broker: ")
        if not conn_info.port:
            temp_port: int = 0
            while temp_port < 1 or temp_port > 65535:
                temp_port = int(input("Port: "))
            conn_info.port = temp_port
        if not conn_info.user_name:
            conn_info.user_name = input("Username: ")
        if not conn_info.password:
            conn_info.password = getpass.getpass("Password:  ")
        if not conn_info.topic:
            conn_info.topic = input("Topic: ")
        save_secrets = input("Save secrets? [y/N]: ")
        # save secrets to file if user wants to
        if save_secrets.lower() == 'y':
            # create the secrets folder if it doesn't exist
            if not os.path.exists(os.path.join(root_dir, "../../secrets")):
                os.mkdir(os.path.join(root_dir, "../../secrets"))
            # save the secrets to file
            with open(secrets_file, 'w', encoding='utf8') as f:
                json.dump(conn_info.__dict__, f, indent=4)

    return conn_info


def create_mqtt_client(conn_info: ConnectionInfo,
                       on_connect: callable = NotImplemented,
                       on_message: callable = NotImplemented) -> mqtt_client.Client:
    """
    Creates an MQTT client with the given connection information.

    Args:
        conn_info (ConnectionInfo): The connection information for the MQTT broker.
        on_connect (callable, optional):
            The callback function to be called when the client connects to the broker.
            Defaults to NotImplemented, in which case a local default function is used.
        on_message (callable, optional):
            The callback function to be called when a message is received.
            Defaults to NotImplemented, in which case a local default function is used.

    Returns:
        mqtt_client.Client: The MQTT client.

    """
    def default_on_connect(_client, _user_data, _flags, return_code, _properties):
        if return_code == 0:
            print(f"Connected to {conn_info.broker}")
        else:
            print(f"Failed to connect, return code {return_code}")

    def default_on_message(_client, _userdata, msg):
        print(f"Message received [{msg.topic}]: {msg.payload}")

    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
                                client_id=f"python-mqtt-time-{random.randint(0, 4095)}")
    client.username_pw_set(conn_info.user_name, conn_info.password)
    # Thank you, Benjamin Helmer Weeke Hervit, for adding to the following line of code
    client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE)

    if on_connect is NotImplemented:
        client.on_connect = default_on_connect
    else:
        client.on_connect = on_connect
    if on_message is NotImplemented:
        client.on_message = default_on_message
    else:
        client.on_message = on_message

    client.connect(conn_info.broker, conn_info.port)
    return client