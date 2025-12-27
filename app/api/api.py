"""
api.py

The fastapi main app.
"""

from fastapi import FastAPI, HTTPException, status

from ..domain.account import AccountStorage
from ..network import get_exchange_rates
from .models import (
    AccountManipulationRequest,
    AccountManipulationResponse,
    RateGetResponse,
    RatesGetResponse,
)

__all__ = []

app = FastAPI(title="Bank Account Manager")
storage = AccountStorage()


@app.get("/accounts/{account_id}", response_model=AccountManipulationResponse)
def get_account_by_id(account_id: int) -> AccountManipulationResponse:
    """
    Returns the account information directly using id.
    """
    account = storage.get_account_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return AccountManipulationResponse(id=account.id, balance=account.get_balance())


@app.post("/accounts/{account_id}/deposit", response_model=AccountManipulationResponse)
def deposit(
    account_id: int, req: AccountManipulationRequest
) -> AccountManipulationResponse:
    """
    Deposits amount into account_id using pin and amount in req
    """
    account = storage.get_account(account_id, req.pin)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong PIN or ID"
        )
    account.deposit(req.amount)
    storage.update_balance(account)
    return AccountManipulationResponse(id=account.id, balance=account.get_balance())


@app.post("/accounts/{account_id}/withdraw", response_model=AccountManipulationResponse)
def withdraw(
    account_id: int, req: AccountManipulationRequest
) -> AccountManipulationResponse:
    """
    Withdraws amount from account_id using pin and amount in req
    """
    account = storage.get_account(account_id, req.pin)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong PIN or ID"
        )
    success, err_message = account.withdraw(req.amount)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_message)
    storage.update_balance(account)
    return AccountManipulationResponse(id=account.id, balance=account.get_balance())


@app.get("/rates", response_model=RatesGetResponse)
def get_rates() -> RatesGetResponse:
    ok, rates, error = get_exchange_rates()
    if not ok or not rates:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=error
        )
    return RatesGetResponse(base="USD", rates=rates)


@app.get("/rates/{currency_code}", response_model=RateGetResponse)
def get_rate(currency_code: str) -> RateGetResponse:
    ok, rates, error = get_exchange_rates()
    if not ok or rates is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=error
        )
    if currency_code.upper() not in rates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Currency Not Found"
        )
    return RateGetResponse(
        base="USD", currency=currency_code.upper(), rate=rates[currency_code.upper()]
    )
