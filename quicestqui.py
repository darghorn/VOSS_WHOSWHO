#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import random


# Update this list to change the name in the answer
list = [u'Paul', u'Lola', u'Urbain', u'Emilio', u'Papi']

# Initialize the random access
secure_random = random.SystemRandom()

# MQTT client to connect to the bus
mqtt_client = mqtt.Client()

# Function to get a slot by name
def slot_decoder(slots, slot_name):
    for slot in slots:
        if slot['slotName'] == slot_name:
            return slot['value']['value']
    return None

def on_connect(client, userdata, flags, rc):
    # subscribe to Domos:Quicestqui messages
    mqtt_client.subscribe('hermes/intent/Domos:Quicestqui')

# Process a message as it arrives
def on_message(client, userdata, msg):
    session_id = "0"
    rep = ""
    if len(msg.payload) > 0:
        message = str(msg.payload.decode('utf8'))
        info=json.loads(message)
        session_id=info["sessionId"]
        if "Quicestqui" in info["intent"]["intentName"]:
            try:
                _qualif = slot_decoder(info["slots"],'qualif')
                _quoi = slot_decoder(info["slots"],'quoi')
                _qui = slot_decoder(info["slots"],'article')
            except:
                _qui = "le"
                _quoi = "fort"
                _qualif = "plus"
            rep = u"" + _qui + " " +_qualif + " " + _quoi + ", c'est "+ secure_random.choice(list)
    else:
        rep="erreur"
    if len(rep)>0:
        mqtt_client.publish('hermes/dialogueManager/endSession', json.dumps({'text': rep, "sessionId" : session_id}))

if __name__ == '__main__':
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('localhost', 1883)
    mqtt_client.loop_forever()
