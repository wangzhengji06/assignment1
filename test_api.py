"""
test_api.py

Used to test the fastapi endpoint call.

"""


def test_get_account_not_found(client):
    resp = client.get("/accounts/1")
    assert resp.status_code == 404


def test_deposit_and_get_balance(client, test_storage):
    test_storage.create_account(
        id=1,
        pin="1234",
        initial_balance=100,
    )

    resp = client.post(
        "/accounts/1/deposit",
        json={"pin": "1234", "amount": 50},
    )

    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "balance": 150}

    resp = client.get("/accounts/1")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "balance": 150}


def test_withdraw_success(client, test_storage):
    test_storage.create_account(
        id=2,
        pin="0000",
        initial_balance=200,
    )

    resp = client.post(
        "/accounts/2/withdraw",
        json={"pin": "0000", "amount": 80},
    )

    assert resp.status_code == 200
    assert resp.json()["balance"] == 120


def test_withdraw_insufficient_balance(client, test_storage):
    test_storage.create_account(
        id=3,
        pin="1111",
        initial_balance=10,
    )

    resp = client.post(
        "/accounts/3/withdraw",
        json={"pin": "1111", "amount": 50},
    )

    assert resp.status_code == 400
    assert resp.json()["detail"] == "Not enough balance"


def test_wrong_pin(client, test_storage):
    test_storage.create_account(
        id=4,
        pin="2222",
        initial_balance=100,
    )

    resp = client.post(
        "/accounts/4/deposit",
        json={"pin": "9999", "amount": 10},
    )

    assert resp.status_code == 401
