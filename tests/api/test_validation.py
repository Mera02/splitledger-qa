from uuid import uuid4


def create_group(api_client):
    response = api_client.post(
        "/api/groups",
        json={
            "name": f"Validation Trip {uuid4().hex[:8]}",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def add_member(
    api_client,
    group_id,
    name,
):
    response = api_client.post(
        f"/api/groups/{group_id}/members",
        json={
            "name": name,
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_accepts_minimum_amount(api_client):
    group_id = create_group(api_client)

    faris_id = add_member(
        api_client,
        group_id,
        "Faris",
    )

    add_member(
        api_client,
        group_id,
        "Ada",
    )

    amar_id = add_member(
        api_client,
        group_id,
        "Amar",
    )

    response = api_client.post(
        f"/api/groups/{group_id}/expenses",
        json={
            "payer_member_id": amar_id,
            "description": "Minimum expense",
            "amount": "0.01",
        },
    )

    assert response.status_code == 201

    balances_response = api_client.get(
        f"/api/groups/{group_id}/balances"
    )

    balances = {
        item["member_name"]:
            item["balance_cents"]
        for item in balances_response.json()
    }

    assert balances == {
        "Faris": -1,
        "Ada": 0,
        "Amar": 1,
    }

    assert sum(balances.values()) == 0


def test_rejects_zero_amount(api_client):
    group_id = create_group(api_client)

    faris_id = add_member(
        api_client,
        group_id,
        "Faris",
    )

    response = api_client.post(
        f"/api/groups/{group_id}/expenses",
        json={
            "payer_member_id": faris_id,
            "description": "Invalid expense",
            "amount": "0.00",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail":
            "Amount must be greater than zero."
    }


def test_rejects_negative_amount(api_client):
    group_id = create_group(api_client)

    faris_id = add_member(
        api_client,
        group_id,
        "Faris",
    )

    response = api_client.post(
        f"/api/groups/{group_id}/expenses",
        json={
            "payer_member_id": faris_id,
            "description": "Invalid expense",
            "amount": "-10.00",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail":
            "Amount must be greater than zero."
    }


def test_rejects_more_than_two_decimal_places(
    api_client,
):
    group_id = create_group(api_client)

    faris_id = add_member(
        api_client,
        group_id,
        "Faris",
    )

    response = api_client.post(
        f"/api/groups/{group_id}/expenses",
        json={
            "payer_member_id": faris_id,
            "description": "Invalid precision",
            "amount": "12.345",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail":
            "Amount cannot have more than two decimal places."
    }


def test_rejects_payer_outside_group(api_client):
    first_group_id = create_group(api_client)

    second_group_id = create_group(api_client)

    outside_member_id = add_member(
        api_client,
        second_group_id,
        "Outside Member",
    )

    add_member(
        api_client,
        first_group_id,
        "Faris",
    )

    response = api_client.post(
        f"/api/groups/{first_group_id}/expenses",
        json={
            "payer_member_id":
                outside_member_id,
            "description": "Invalid payer",
            "amount": "20.00",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail":
            "Payer must belong to the group."
    }


def test_rejects_duplicate_member_name(api_client):
    group_id = create_group(api_client)

    add_member(
        api_client,
        group_id,
        "Faris",
    )

    response = api_client.post(
        f"/api/groups/{group_id}/members",
        json={
            "name": "  FARIS  ",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail":
            "Member already exists in this group."
    }