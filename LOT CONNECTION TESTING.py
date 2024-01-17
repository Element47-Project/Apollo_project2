from azure.iot.device import IoTHubDeviceClient, Message
import json
from datetime import datetime

def send_message_to_iot_hub():
    conn_str = ("HostName=Element47.azure-devices.net;DeviceId=Element47;"
                "SharedAccessKey=eFaZPtSBWZFGPbyYvxW7QVTxGd6+qSlSVAIoTKxYzD8=")
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
