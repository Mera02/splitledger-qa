from uuid import uuid4


def test_complete_equal_split_flow(api_client):
    group_name = f"QA Trip {uuid4().hex[:8]}"

    group_response = api_client.post(
        "/api/groups",
        json={
            "name": group_name,
        },
    )

    assert group_response.status_code == 201

    group_id = group_response.json()["id"]

    member_ids = {}

    for name in ["Faris", "Ada", "Amar"]:
        response = api_client.post(
            f"/api/groups/{group_id}/members",
            json={
                "name": name,
            },
        )

        assert response.status_code == 201

        member_ids[name] = response.json()["id"]

    expense_response = api_client.post(
        f"/api/groups/{group_id}/expenses",
        json={
            "payer_member_id":
                member_ids["Faris"],
            "description": "Apartment",
            "amount": "100.00",
        },
    )

    assert expense_response.status_code == 201

    balances_response = api_client.get(
        f"/api/groups/{group_id}/balances"
    )

    assert balances_response.status_code == 200

    balances = {
        item["member_name"]:
            item["balance_cents"]
        for item in balances_response.json()
    }

    expected_balances = {
        "Faris": 6666,
        "Ada": -3333,
        "Amar": -3333,
    }

    assert balances == expected_balances
    assert sum(balances.values()) == 0

    settlements_response = api_client.get(
        f"/api/groups/{group_id}/settlements"
    )

    assert settlements_response.status_code == 200

    settlements = settlements_response.json()

    expected_settlements = [
        {
            "from_member_id":
                member_ids["Ada"],
            "from_member_name": "Ada",
            "to_member_id":
                member_ids["Faris"],
            "to_member_name": "Faris",
            "amount_cents": 3333,
        },
        {
            "from_member_id":
                member_ids["Amar"],
            "from_member_name": "Amar",
            "to_member_id":
                member_ids["Faris"],
            "to_member_name": "Faris",
            "amount_cents": 3333,
        },
    ]

    assert settlements == expected_settlements