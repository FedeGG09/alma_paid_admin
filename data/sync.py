# data/sync.py
import requests
from data.repository import SQLiteRepository, Student

API = "https://almapaid.streamlit.app/"

def sync_pull():
    r = requests.get(f"{API}/all")
    if r.status_code == 200:
        repo = SQLiteRepository()
        for item in r.json():
            s = Student(
                id=item['id'], name=item['name'], email=item['email'],
                dni=item['dni'], status=item['status']
            )
            # repo.upsert_student(s)
