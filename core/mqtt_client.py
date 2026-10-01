import paho.mqtt.client as mqtt
from typing import Callable, Optional


class MqttManager:
    def __init__(self, broker: str, port: int, client_id: str = "cae_verifier"):
        self.broker = broker
        self.port = port
        self.client_id = client_id

        # Поддержка новой версии API paho-mqtt
        try:
            self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.V2, client_id=self.client_id)
        except AttributeError:
            self.client = mqtt.Client(client_id=self.client_id)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        self.on_message_callback: Optional[Callable[[str, str], None]] = None
        self.is_connected = False

    def connect(self) -> bool:
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Ошибка MQTT: {e}")
            return False

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.is_connected = True
            self.client.subscribe("esp32/cam1/#")
            print("MQTT подключен")

    def _on_disconnect(self, client, userdata, rc, properties=None):
        self.is_connected = False
        print("MQTT отключен")

    def _on_message(self, client, userdata, msg):
        if self.on_message_callback:
            self.on_message_callback(msg.topic, msg.payload.decode('utf-8'))

    def publish(self, topic: str, payload: str):
        if self.is_connected:
            self.client.publish(topic, payload)

    def set_callback(self, callback: Callable[[str, str], None]):
        self.on_message_callback = callback

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()