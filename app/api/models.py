"""
models.py

Used to define the dataclass for fastapi
"""

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Field

__all__ = []


class AccountManipulationResponse(BaseModel):
    """
    The dataclass that defines the response to get or post request
    """

    id: int
    balance: int


class RatesGetResponse(BaseModel):
    """
    The dataclass that defines the response to get rates
    """

    base: str
    rates: Dict[str, float]


class RateGetResponse(BaseModel):
    """
    The dataclass that defines the responses to get currency code.
    """

    base: str
    currency: str
    rate: float


class AccountManipulationRequest(BaseModel):
    """
    The dataclass that defines the request body for deposit and withdraw requests.
    """

    pin: str
    amount: int = Field(ge=1)
