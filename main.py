from flask import Flask,render_template
from flask_table import Table, Col
from flask_mqtt import Mqtt
import ast,json
system=0
cpu=0
memory=0
swap=0
disk=0
network=0
speed=0
app = Flask(__name__)
mqtt = Mqtt(app)
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')
@app.route('/')
def data():
    global system,cpu,memory,swap,disk,network,speed
    templateData = {'system': system,'cpu': cpu,'memory': memory,'swap': swap,'disk': disk,'network': network,'speed': speed,}
    return render_template('hello.html',**templateData)
mqtt.subscribe('topic/sys')
mqtt.subscribe('topic/CPU')
mqtt.subscribe('topic/memory')
mqtt.subscribe('topic/swap')
mqtt.subscribe('topic/disk')
mqtt.subscribe('topic/network')
mqtt.subscribe('topic/speed')

@mqtt.on_topic('topic/sys')
def handle_mysystem(client, userdata, message):
    global system
    system = json.loads(message.payload)
    system=ItemTable(system)

@mqtt.on_topic('topic/CPU')
def handle_mycpu(client, userdata, message):
    global cpu
    cpu = json.loads(message.payload)
    cpu=ItemTable(cpu)

@mqtt.on_topic('topic/memory')
def handle_mymemory(client, userdata, message):
    global memory
    memory = json.loads(message.payload)
    memory=ItemTable(memory)

@mqtt.on_topic('topic/swap')
def handle_myswap(client, userdata, message):
    global swap
    swap = json.loads(message.payload)
    swap=ItemTable(swap)

@mqtt.on_topic('topic/disk')
def handle_mydisk(client, userdata, message):
    global disk
    disk = json.loads(message.payload)
    disk=ItemTable(disk)

@mqtt.on_topic('topic/network')
def handle_mynetwork(client, userdata, message):
    global network
    network = json.loads(message.payload)
    network=ItemTable(network)

@mqtt.on_topic('topic/speed')
def handle_myspeed(client, userdata, message):
    global speed
    speed = json.loads(message.payload)
    speed=ItemTable(speed)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
