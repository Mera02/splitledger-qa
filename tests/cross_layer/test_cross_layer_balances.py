import json
from uuid import uuid4

import httpx
from playwright.sync_api import Page, expect


API_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:5173"


def test_balances_match_across_api_cli_and_ui(
    page: Page,
    run_live_cli,
):
    group_name = (
        f"Cross Layer QA {uuid4().hex[:8]}"
    )

    expected_balances = {
        "Faris": 6666,
        "Ada": -3333,
        "Amar": -3333,
    }

    # -------------------------
    # Arrange through the API
    # -------------------------

    group_response = httpx.post(
        f"{API_URL}/api/groups",
        json={
            "name": group_name,
        },
    )

    assert group_response.status_code == 201

    group_id = group_response.json()["id"]

    member_ids = {}

    for name in ["Faris", "Ada", "Amar"]:
        response = httpx.post(
            f"{API_URL}/api/groups/{group_id}/members",
            json={
                "name": name,
            },
        )

        assert response.status_code == 201

        member_ids[name] = response.json()["id"]

    expense_response = httpx.post(
        f"{API_URL}/api/groups/{group_id}/expenses",
        json={
            "payer_member_id":
                member_ids["Faris"],
            "description": "Apartment",
            "amount": "100.00",
        },
    )

    assert expense_response.status_code == 201

    # -------------------------
    # Verify through the API
    # -------------------------

    api_response = httpx.get(
        f"{API_URL}/api/groups/{group_id}/balances"
    )

    assert api_response.status_code == 200

    api_balances = {
        item["member_name"]:
            item["balance_cents"]
        for item in api_response.json()
    }

    assert api_balances == expected_balances

    # -------------------------
    # Verify through the CLI
    # -------------------------

    cli_result = run_live_cli(
        "balances",
        group_id,
        "--json",
    )

    assert cli_result.returncode == 0

    cli_balances = {
        item["member_name"]:
            item["balance_cents"]
        for item in json.loads(
            cli_result.stdout
        )
    }

    assert cli_balances == expected_balances

    # -------------------------
    # Verify through the UI
    # -------------------------

    page.goto(FRONTEND_URL)

    page.get_by_role(
        "button",
        name=group_name,
        exact=True,
    ).click()

    balances_section = page.locator(
        "section"
    ).filter(
        has=page.get_by_role(
            "heading",
            name="Balances",
        )
    )

    expected_ui_balances = {
        "Faris": "+66.66 KM",
        "Ada": "-33.33 KM",
        "Amar": "-33.33 KM",
    }

    for member_name, amount in (
        expected_ui_balances.items()
    ):
        row = balances_section.locator(
            ".balance-row"
        ).filter(
            has_text=member_name
        )

        expect(row).to_contain_text(
            amount
        )