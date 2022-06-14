# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import sys
import logging
import re
from typing import Text, Dict, Any


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from py2neo import Graph
from markdownify import markdownify as md


logger = logging.getLogger(__name__)
p = "data/lookup/Device.txt"
device_names = [i.strip() for i in open(p, 'r', encoding='UTF-8').readlines()]
def retrieve_device_name(name):
    names = []
    name = '.*' + '.*'.join(list(name)) + '.*'
    pattern = re.compile(name)
    for i in device_names:
        candidate = pattern.search(i)
        if candidate:
            names.append(candidate.group())
    return names

class ActionFirst(Action):
    def name(self) -> Text:
        return "action_first"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        # dispatcher.utter_template("utter_first", tracker)
        # print('ActionFirst'*10)
        dispatcher.utter_message(template="utter_first")
        # dispatcher.utter_template("utter_howcanhelp", tracker)
        # print('dispatcher.utter_message')
        dispatcher.utter_message(md("您可以这样向我提问: <br/>分析[ip]的[cpu]情况<br/>\
                              [ip]有无报警<br/>\
                              什么是[液冷]"))
        return []

# 分析设备的状态
class ActionAnalyseDevice(Action):
    def name(self) -> Text:
        return "utter_analyse_device"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        device = tracker.get_slot("device")
        possible_device = retrieve_device_name(device)
        dispatcher.utter_message(possible_device)
        dispatcher.utter_message(md("分析设备信息？别问问题了！"))


