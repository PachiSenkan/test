import uuid
import random


def test_get_wallets(test_app):
    response = test_app.get("/api/v1/wallets")
    assert response.status_code == 200
    assert len(response.json()) > 1


def test_get_wallet_balance(test_app):
    wallet_id = test_app.get("/api/v1/wallets").json()[0]["id"]
    response = test_app.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    assert response.json()["balance"] >= 0


def test_get_wallet_balance_invalid_uuid(test_app):
    random_wallet_uuid = uuid.uuid4()
    response = test_app.get(f"/api/v1/wallets/{random_wallet_uuid}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Wallet with UUID: {random_wallet_uuid} not found"
    }


def test_get_wallet_balance_invalid_uuid_type(test_app):
    invalid_type_wallet_uuid = "random_string_for_test"
    response = test_app.get(f"/api/v1/wallets/{invalid_type_wallet_uuid}")
    assert response.status_code == 422


def test_wallet_operation_deposit(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id, wallet_prev_balance = wallet["id"], wallet["balance"]
    added_amount = random.random()
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "DEPOSIT", "amount": added_amount},
    )
    assert response.status_code == 200
    assert response.json()["balance"] == wallet_prev_balance + added_amount


def test_wallet_operation_deposit_invalid_uuid(test_app):
    random_wallet_uuid = uuid.uuid4()
    withdrawed_amount = random.random()
    response = test_app.post(
        f"/api/v1/wallets/{random_wallet_uuid}/operation",
        json={"operation": "DEPOSIT", "amount": withdrawed_amount},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Wallet with UUID: {random_wallet_uuid} not found"
    }


def test_wallet_operation_deposit_negative_amount(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id = wallet["id"]
    added_amount = -random.random()
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "DEPOSIT", "amount": added_amount},
    )
    assert response.status_code == 422


def test_wallet_operation_deposit_not_float_number(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id = wallet["id"]
    added_amount = "string_type"
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "DEPOSIT", "amount": added_amount},
    )
    assert response.status_code == 422


def test_wallet_operation_withdraw(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id, wallet_prev_balance = wallet["id"], wallet["balance"]
    withdrawed_amount = random.random()
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "WITHDRAW", "amount": withdrawed_amount},
    )
    assert response.status_code == 200
    assert response.json()["balance"] == wallet_prev_balance - withdrawed_amount


def test_wallet_operation_withdraw_invalid_uuid(test_app):
    random_wallet_uuid = uuid.uuid4()
    withdrawed_amount = random.random()
    response = test_app.post(
        f"/api/v1/wallets/{random_wallet_uuid}/operation",
        json={"operation": "WITHDRAW", "amount": withdrawed_amount},
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Wallet with UUID: {random_wallet_uuid} not found"
    }


def test_wallet_operation_withdraw_more_than_balance(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id, wallet_prev_balance = wallet["id"], wallet["balance"]
    withdrawed_amount = wallet_prev_balance + 100
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "WITHDRAW", "amount": withdrawed_amount},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"Max withdraw amount is {wallet_prev_balance}"
    }


def test_wallet_operation_withdraw_negative_amount(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id = wallet["id"]
    added_amount = -random.random()
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "WITHDRAW", "amount": added_amount},
    )
    assert response.status_code == 422


def test_wallet_operation_withdraw_not_float_number(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id = wallet["id"]
    added_amount = "string_type"
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "WITHDRAW", "amount": added_amount},
    )
    assert response.status_code == 422


def test_wallet_operation_not_available_operation(test_app):
    wallet = test_app.get("/api/v1/wallets").json()[0]
    wallet_id = wallet["id"]
    added_amount = random.random()
    response = test_app.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation": "NOTAVAILABLEOPERATION", "amount": added_amount},
    )
    assert response.status_code == 422
