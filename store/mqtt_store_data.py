"""Mqtt store data from sensor to database."""
import json
import os.path
import signal
import sys

from paho.mqtt import client as mqtt_client

from sensordb import SensorDataSQLite3db
from connectioninfo import ConnectionInfo, get_secrets, create_mqtt_client


def run(client: mqtt_client.Client) -> None:
    """Start the client and run it forever until ctrl-c

    Args:
        client (mqtt_client.Client): the MQTT client
    """

    # function to handle ctrl-c
    def signal_handler(_sig, _frame):
        print("You pressed Ctrl+C!")
        client.disconnect()
        sys.exit(0)

    # register the signal handlers
    signal.signal(signal.SIGINT, signal_handler)

    # start the client and run it until ctrl-c
    client.loop_forever()


if __name__ == "__main__":
    connection_info = ConnectionInfo(broker='myggen.mooo.com',
                                     port=8883, topic='au591396/sensor')

    connection_info = get_secrets(connection_info,  __file__)
    # Get the root directory of this file
    root_dir = os.path.abspath(os.path.dirname(__file__))
    # Set the path to the database
    sqlite3_db = os.path.join(root_dir, "mqtt_data.db")

    database = SensorDataSQLite3db(sqlite3_db)

    def on_connect(client, _userdata, _flags, return_code, _properties) -> None:
        """
        Callback function that is called when the client successfully connects to the MQTT broker.

        Parameters:
        - client: The MQTT client instance.
        - _userdata: The user data associated with the client (not used in this function).
        - _flags: The flags associated with the connection (not used in this function).
        - return_code: The return code from the connection attempt.

        Returns:
        None
        """
        if return_code == 0:
            print(f"Connected to {connection_info.broker}")
            client.subscribe(connection_info.topic)
        else:
            print(f"Failed to connect, return code {return_code}")

    def on_message(_client, _userdata, msg) -> None:
        """
        Callback function that is called when a message is received.

        Parameters:
        - _client: The MQTT client object.
        - _userdata: Any user-defined data associated with the client.
        - msg: The received message object.

        Returns:
        None

        Description:
        This function is responsible for processing the received message and storing the dice throw
        in the database.
        It prints the received message and then calls the `store_throw` function from the `dicedb`
        module to store the throw.

        """
        data = json.loads(msg.payload)
        print(f"Message received [{msg.topic}]: {data}")

        # Ensure that 'throw' is a dictionary and contains the necessary keys
        if isinstance(data, dict) and 'eCO2' in data and 'TVOC' in data:
            database.insert_data(data)
        else:
            print("Invalid payload received")

    run(create_mqtt_client(connection_info,
        on_connect=on_connect, on_message=on_message))
