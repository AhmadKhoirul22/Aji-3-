# import hitung mtk
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re
# import cuaca
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

# hitung mtk
class ActionCalculate(Action):

    def name(self) -> Text:
        return "action_calculate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Ambil ekspresi dari user input
        user_message = tracker.latest_message['text']
        match = re.search(r'\d+\s*[\+\-\*/]\s*\d+', user_message)

        if match:
            expression = match.group(0)
            try:
                # Hitung hasil ekspresi
                result = eval(expression)
                response = f"Hasil dari perhitungan {expression} adalah {result}"
            except Exception as e:
                response = "Maaf, saya tidak bisa menghitung itu."
        else:
            response = "Saya tidak menemukan perhitungan yang valid di input Anda."

        dispatcher.utter_message(text=response)
        return []

# cuaca
class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Ambil lokasi dari entitas
        location = next(tracker.get_latest_entity_values("location"), None)

        if location:
            api_key = "df55f7b31d6c4f203e9fb724fd9af49c"  # Ganti dengan API Key OpenWeatherMap Anda
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]

                response_message = (f"Cuaca di {location} saat ini adalah {description} "
                                    f"dengan suhu {temperature}°C.")
            else:
                response_message = f"Maaf, saya tidak dapat menemukan informasi cuaca untuk {location}."
        else:
            response_message = "Silakan sebutkan lokasi yang ingin Anda ketahui cuacanya."

        dispatcher.utter_message(text=response_message)
        return []