# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

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
from markdownify import markdownify as md


logger = logging.getLogger(__name__)
device_path = "data/lookup/Device_name.txt"
device_names = [i.strip() for i in open(device_path, 'r', encoding='UTF-8').readlines()]
level1 = ["os_machine_value", "power_value","temperature_value"]
level2 = {
    "os_machine_value":["CPU_IDLE","MEM_USED_PERCENT"],
    "power_value":["CPU_Total_Power_value" ,"MEM_Total_Power_value" ,"Total_Power_value"],
    "temperature_value":["CPU0_Temp_value" ,"CPU0_VR_Temp_value","CPU1_Temp_value","CPU1_VR_Temp_value" ,"DIMMG1_Temp_value","DIMMG0_Temp_value" ,"Inlet_Temp_value" ,"Outlet_Temp_value" ,"PCH_Temp_value","PSU0_Temp_value" ,"PSU1_Temp_value"]}
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

def make_button(title,payload):
    return {'title': title, 'payload': payload}

# 分析设备的状态
class ActionAnalyseDevice(Action):
    def name(self) -> Text:
        return "utter_analyse_device"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        device = tracker.get_slot("device_name")
        possible_device = retrieve_device_name(device)
        buttons = []
        for d in level1:
            buttons.append(make_button(d, '/search_level2{{"analyse_level1":"{0}", "sure":"{1}"}}'.format(d, d)))
        dispatcher.utter_button_message("请点击选择想查询的具体内容", buttons)
        return []

def ActionSearchLevel1(Action):
    def name(self) -> Text:
        return "utter_search_level2"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        level1_name = tracker.get_slot("analyse_level1")
        buttons = []
        for b in level2[level1_name]:
            buttons.append(make_button(b, '/analyse_device_final{{"analyse_level2":"{0}", "sure":"{1}"}}'.format(b, b)))
        dispatcher.utter_button_message("请点击选择想查询的具体内容", buttons)
        return []

def ActionAnalyseDeviceFinal(Action):
    def name(self) -> Text:
        return "utter_analyse_device_final"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        device_name = tracker.get_slot("device_name")
        level1_name = tracker.get_slot("analyse_level1")
        level2_name = tracker.get_slot("analyse_level2")
        dispatcher.utter_button_message("查询设备名称{0}上的{1}{2}情况信息".format(device_name,level1_name,level2_name))
        return []


