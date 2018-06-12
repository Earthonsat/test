#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import random

def subscribe_intent_callback(hermes, intentMessage):
    action_wrapper(hermes, intentMessage)

def action_wrapper(hermes, intentMessage):
    blagues = ["c'est l'histoire d'un zoophile qui rentre dans un bar.","qu'est-ce qui est jaune et qui attend ? Jonathan.","désolé, je ne suis pas d'humeur blagueuse aujourd'hui.","je ne connais pas encore assez de blagues, désolé."]
    result_sentence = random.choice(blagues)
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("jumahe:blague", subscribe_intent_callback).start()
