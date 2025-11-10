"""
network.py

Call the api and get the exchange rate
save the cache into a json file
Updated every 24 hours
"""

import json
import os
import time
from typing import Dict

import requests

__all__ = ["get_exchange_rates"]

API_KEY = os.getenv("EXCHANGE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing EXCHANGE_API_KEY")

API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
CACHE_FILE = "exchange_cache.json"
CACHE_TTL = 24 * 60 * 60


def load_cache() -> Dict[str, int] | None:
    """
    If file not exists or over 24 hours, return None
    Else load json, read 'rates' and return dict
    """
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, "r") as f:
        data = json.load(f)
    if time.time() - data["timestamp"] > CACHE_TTL:
        return None
    return data["rates"]


def save_cache(rates) -> None:
    """
    Dump the json to file
    """
    with open(CACHE_FILE, "w") as f:
        json.dump({"timestamp": time.time(), "rates": rates}, f)


def get_exchange_rates() -> Dict[str, int]:
    """
    Return the exchange rate dict
    """
    cache_rates = load_cache()
    if cache_rates:
        return cache_rates
    resp = requests.get(API_URL)
    resp.raise_for_status()
    data = resp.json()["conversion_rates"]

    save_cache(data)
    return data
