import requests
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv(".env")

APP_ID = os.getenv("APP_ID_WORKOUT")
print(APP_ID)
API_KEY = os.getenv("API_KEY")
BEARER = os.getenv("BEARER")

nutri_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
user_input= input("Tell Me Which Exercise you did today\n")

today = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%X")

birth_date_str = '31/05/91'
birth_date_obj = datetime.strptime(birth_date_str, '%d/%m/%y')

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

GENDER = os.getenv("GENDER")
WEIGHT_KG = os.getenv("WEIGHT_KG")
HEIGHT_CM = os.getenv("HEIGHT_CM")
AGE = calculate_age(birth_date_obj)

print(AGE)

query = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "x-app-id" : APP_ID,
    "x-app-key" : API_KEY,
    'x-remote-user-id': '0',
}

response = requests.post(url=nutri_endpoint, data=query, headers=headers)
response.raise_for_status()
response = response.json()
print(response)
exercises = response['exercises']
print(exercises)

sheets_header = {
    "Authorization": f"Bearer {BEARER}",
    "Content-Type": "application/json",
}

sheets_url = "https://api.sheety.co/22b8a84df14a589aabfab6a9ff4d57da/myWorkouts/workouts/"

response_sheets = requests.get(url=sheets_url, headers=sheets_header)
response_sheets.raise_for_status()

for exercise in exercises:
    workouts = {
        'workout': {
            "date": today,
            "time": time,
            "exercise": exercise['user_input'],
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
    }}

print(workouts)

response_sheets = requests.post(url=sheets_url, json=workouts)
print(response_sheets.text)
response_sheets.raise_for_status()
print(response_sheets.json())

# delete_sheets = requests.delete("https://api.sheety.co/22b8a84df14a589aabfab6a9ff4d57da/myWorkouts/workouts/2")
# delete_sheets.raise_for_status()
