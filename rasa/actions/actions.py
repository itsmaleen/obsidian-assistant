from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime as dt
import requests


# Need to run `rasa run actions` concurrently

class ActionListGoals(Action):

    def name(self) -> Text:
        return "action_list_goals"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time = tracker.get_slot("time")
        time_object = dt.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")
        # Use docker container name
        response = requests.get('http://knowledge-interaction:5000/goals',
                                data={'date': time_object.strftime("%Y-%m-%d")})

        print(response.status_code)
        if response.status_code != 200:
            dispatcher.utter_message(text="Sorry, something went wrong")
            return []

        dispatcher.utter_message(text=response.text)

        return []
