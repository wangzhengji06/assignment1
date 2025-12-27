"""
network.py

Call the api and get the exchange rate
save the cache into a json file
Updated every 24 hours
"""

import json
import os
import time
from typing import Dict, Optional, Tuple

import requests
from dotenv import load_dotenv

__all__ = ["get_exchange_rates"]

API_URL = "https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
CACHE_FILE = "exchange_cache.json"
CACHE_TTL = 24 * 60 * 60


# Add an api client
# load_cahce and save cache are private methods
def load_cache() -> Dict[str, float] | None:
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


def get_exchange_rates(
    base: str = "USD", timeout: float = 5.0
) -> Tuple[bool, Optional[Dict[str, float]], Optional[str]]:
    """
    Returns (ok, rates, error). Uses cache first. On failure, (False, None, 'message').
    """
    # Move the following two lines to main.py
    load_dotenv()
    key = os.getenv("EXCHANGE_API_KEY")
    if not key:
        # still allow cache use if present
        cached = load_cache()
        return (False, cached, "Missing EXCHANGE_API_KEY")

    cached = load_cache()
    if cached:
        return (True, cached, None)

    try:
        resp = requests.get(API_URL.format(API_KEY=key, base=base), timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        rates = data.get("conversion_rates")
        if not isinstance(rates, dict):
            return (False, cached, "Bad API response")
        rates = {k: float(v) for k, v in rates.items()}
        save_cache(rates)
        return (True, rates, None)
    except requests.Timeout:
        return (False, cached, "Network timeout")
    except requests.RequestException as e:
        return (False, cached, f"Network error: {e}")
