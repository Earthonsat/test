#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
from time import sleep
from RPi import GPIO

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
    action_wrapper(hermes, intentMessage, conf)

def action_wrapper(hermes, intentMessage, conf):
    current_session_id = intentMessage.session_id
    GPIO.output(14, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(14, GPIO.LOW)
    sleep(0.5)
    GPIO.output(14, GPIO.HIGH)
    sleep(1)
    GPIO.output(14, GPIO.LOW)
    sleep(1)
    GPIO.output(14, GPIO.HIGH)
    sleep(0.5)
    GPIO.output(14, GPIO.LOW)
    result_sentence = "H, E, L, L, O, FRIENDS !"
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    GPIO.output(14, GPIO.LOW)
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("jumahe:disco-light", subscribe_intent_callback).start()
