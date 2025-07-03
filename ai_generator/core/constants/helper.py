import random
from typing import List
from core.constants.story_metadata import GENRES, TONES
import httpx

LATIN_NATS = "AU,BR,CA,CH,DE,DK,ES,FI,FR,GB,IE,NL,NZ,US,IN"


def fetch_random_names(num_names=5):
    try:
        response = httpx.get(
            f"https://randomuser.me/api/?results={num_names}&nat={LATIN_NATS}"
            , timeout=5.0
        )
        response.raise_for_status()
        users = response.json()["results"]
        names = [
            f"{user['name']['first']} {user['name']['last']}\nAge:{user['dob']['age']}\nGender: {user['gender']}\nNationality: {user['nat']}\n\n"
            for user in users
        ]
        return names
    except httpx.RequestError as e:
        print(f"[fetch_random_names] Error: {e}")
        return []


def random_genre() -> List[str]:
    return random.choices(GENRES, k=2)


def random_tone() -> str:
    return random.choice(TONES)
