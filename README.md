# SAMS
I am running the MQTT server locally
Findout how to run MQTT server locally.
There are two python files to be run simultaneously- Main.py (on the server)
sys.py(on the client device)
Here i will am using a Raspberry pi as the client device
Clone the repository on both the devices.
Follow the below commands for both client and server-

$ pipenv shell 
$ pip install -r requirements.txt

Edit the sys.py file to add the IP address of the MQTT server.

On the server side:
$ pipenv shell 
(to load the virtual environment)
$ python main.py
(will run the flask server on 0.0.0.0:80)
open the ip address on which the server is running using some browser

On the client side:
$ pipenv shell 
(to load the virtual environment)
$ python sys.py
