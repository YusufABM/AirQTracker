"""
A demo of subscribing to MQTT using the Paho MQTT client and TLS,
with login details stored in a JSON file
"""
from dataclasses import dataclass
import getpass
import json
import os
import os.path
import random
import signal
import ssl
import sys

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



def create_mqtt_client(conn_info: ConnectionInfo) -> mqtt_client.Client:
    """
    Creates an MQTT client and sets up the necessary callbacks and connection parameters.

    Args:
        conn_info (ConnectionInfo): An object containing the connection information.

    Returns:
        mqtt_client.Client: The created MQTT client.

    """
    def on_connect(client, _user_data, _flags, return_code, _properties):
        if return_code == 0:
            print(f"Connected to {conn_info.broker}")
            client.subscribe(conn_info.topic)
        else:
            print(f"Failed to connect, return code {return_code}")

    def on_message(_client, _userdata, msg):
        print(f"Message received [{msg.topic}]: {json.loads(msg.payload)}")

    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
                                client_id=f"python-mqtt-sub-{random.randint(0, 4095)}")
    client.username_pw_set(conn_info.user_name, conn_info.password)
    client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(conn_info.broker, conn_info.port)
    return client


def run(client: mqtt_client.Client) -> None:
    """Start the client and run it forever until ctrl-c

    Args:
        client (mqtt_client.Client): the MQTT client
    """
     # function to handle incoming messages
    def on_message(client, userdata, message):
        print(f"Received message '{message.payload}' on topic '{message.topic}' with QoS {message.qos}")

    client.on_message = on_message


    # function to handle ctrl-c
    def signal_handler(_sig, _frame):
        print("You pressed Ctrl+C!")
        client.disconnect()
        sys.exit(0)

    # register the signal handlers
    signal.signal(signal.SIGINT, signal_handler)

    # start the client and run it until ctrl-c
    client.loop_forever()


def get_secrets(conn_info: ConnectionInfo):
    """
    Retrieves the MQTT connection secrets from a secrets file or prompts the user to enter them.

    Args:
        conn_info (ConnectionInfo): An instance of the ConnectionInfo class
        that holds the connection information.

    Returns:
        ConnectionInfo: The updated connection_info object with the retrieved or entered secrets.
    """

    # get the path to this Python file
    root_dir = os.path.abspath(os.path.dirname(__file__))
    # get the name of this Python file without the .py extension
    this_file = os.path.basename(__file__)[:-3]
    # create the path to the secrets file, one level up from this file
    secrets_file = os.path.join(
        root_dir, f"../secrets/{this_file}_secrets.json")

    # load secrets from file if it exists
    if os.path.exists(secrets_file):
        with open(secrets_file, 'r', encoding='utf8') as f:
            conn_info.update(json.load(f))
    else:
        # otherwise ask for them
        conn_info.user_name = input("Username: ")
        conn_info.password = getpass.getpass("Password:  ")
        conn_info.topic = input("Topic: ")
        save_secrets = input("Save secrets? [y/N]: ")
        # save secrets to file if user wants to
        if save_secrets.lower() == 'y':
            # create the secrets folder if it doesn't exist
            if not os.path.exists(os.path.join(root_dir, "../secrets")):
                os.mkdir(os.path.join(root_dir, "../secrets"))
            # save the secrets to file
            with open(secrets_file, 'w', encoding='utf8') as f:
                json.dump(conn_info.__dict__, f, indent=4)

    return conn_info


if __name__ == "__main__":
    connection_info = ConnectionInfo(broker='myggen.mooo.com', port=8883)
    connection_info = get_secrets(connection_info)

    run(create_mqtt_client(connection_info))