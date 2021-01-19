# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet,AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.third_weather import get_weather_by_day
from actions.check_travel import get_travel_info

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
def get_text_weather_date(address, date_time, date_time_number):
    try:
        result = get_weather_by_day(address, date_time_number)
    except Exception as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """
            {} {} ({}) 的天气情况为：白天：{}；夜晚：{}；气温：{}-{} °C
        """
        text_message = text_message_tpl.format(
            result['location']['name'],
            date_time,
            result['result']['date'],
            result['result']['text_day'],
            result['result']['text_night'],
            result['result']["high"],
            result['result']["low"],
        )

    return text_message

def text_date_to_number_date(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return text_date

    if text_date.startswith("星期"):
        # @todo: using calender to compute relative date
        return text_date

    if text_date.startswith("下星期"):
        # @todo: using calender to compute relative date
        return text_date

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return text_date
    if text_date == "前天":
        return text_date
    if text_date == "大前天":
        return text_date

class TravelForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "travel_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["city"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        city = tracker.get_slot('city')
        #查接口。。。。---->travel_list
        print(city)
        # if not city:
        #     city="云南"
        if city:
            travel_list=get_travel_info(city)
            if travel_list:
                travel_data ="{}的景点：{}".format(city,travel_list)
            else:
                travel_data=f"小芯没能为您找到 {city} 的景点~"
            dispatcher.utter_message(travel_data)
        return [AllSlotsReset()]

# class WeatherForm(FormAction):
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#
#         return "weather_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#
#         return ["date_time", "address"]
#
#     def submit(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         address = tracker.get_slot('address')
#         date_time = tracker.get_slot('date_time')
#
#         date_time_number = text_date_to_number_date(date_time)
#
#         if isinstance(date_time_number, str):  # parse date_time failed
#             dispatcher.utter_message("暂不支持查询 {} 的天气".format([address, date_time_number]))
#         else:
#             weather_data = get_text_weather_date(address, date_time, date_time_number)
#             dispatcher.utter_message(weather_data)
#         return []