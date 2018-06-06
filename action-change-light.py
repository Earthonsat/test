#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from RPi import GPIO
#import logging

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    #logging.debug('intent subscribed')
    action_wrapper(hermes, intentMessage, conf)
    #action_wrap(hermes, intentMessage)

def action_wrapper(hermes, intentMessage, conf):
    #logging.debug('action wrapper')
    result_sentence = "Bonjour le monde."
    if len(intentMessage.slots.state) > 0:
        state = intentMessage.slots.state.first().value
        if state == "on":
            result_sentence = "OK, allumage de la lampe."
            GPIO.output(14, GPIO.HIGH)
        else:
            result_sentence = "Compris, j'éteins la lampe."
            GPIO.output(14, GPIO.LOW)
    else:
        result_sentence = "Nope"
    ​
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

def action_wrap(hermes, intentMessage):
    result_sentence = "Bonjour le monde."
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
    #logging.basicConfig(filename='/home/pi/debug.log',level=logging.DEBUG)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, GPIO.LOW)
    #logging.debug('READY')
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("jumahe:change-light", subscribe_intent_callback).start()
