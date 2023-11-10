from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
import paho.mqtt.client as mqtt, dotenv, os, time 


def portAndKeys():
    global mqttHost
    global mqttPort
    global mqttTopic

    dotenv.load_dotenv()

    mqttHost = os.environ.get("Host")
    mqttPort = int(os.environ.get("Port"))
    mqttTopic = 'Bedroom'


def enviroPayload(sensor,light):
    light.update_sensor()
    datetimeATM= int(time.time())
    temperature = sensor.get_temperature()
    humidity=sensor.get_humidity()
    pressure=sensor.get_pressure()
    lux=light.get_lux()
    return f'{{"Datetime":{datetimeATM},"Tempature":{temperature},"Humidity":{humidity},"Pressure":{pressure},"Lux":{lux}}}'



def mqttPusher(userHost, userPort, topic,payload):
    client=mqtt.Client()
    client.connect(host=userHost, port=userPort)
    client.publish(topic,payload)

portAndKeys()
payload = enviroPayload(BME280(i2c_dev= SMBus(1)),LTR559())
mqttPusher(mqttHost, mqttPort, mqttTopic, payload)
