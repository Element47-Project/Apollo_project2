from azure.iot.device import IoTHubDeviceClient, Message
import json
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()


def send_message_to_iot_hub():
    host_name = os.environ.get('Host_Name')
    device_id = os.environ.get('Device_ID')
    primary_key = os.environ.get('Primary_key')
    conn_str = (f"HostName={host_name};DeviceId={device_id};"
                f"{primary_key}")
    client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    try:
        message_dict = {
            "message": "Helloooo!",
            "timestamp": datetime.now().isoformat()
        }
        message_json = json.dumps(message_dict)
        msg = Message(message_json)
        msg.content_type = "application/json"
        msg.content_encoding = "utf-8"
        client.send_message(msg)
        print("Message successfully sent", message_json)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.shutdown()


send_message_to_iot_hub()
