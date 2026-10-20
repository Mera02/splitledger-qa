import json


def test_complete_cli_flow(run_cli):
    group_result = run_cli(
        "group-create",
        "QA CLI Trip",
        "--json",
    )

    assert group_result.returncode == 0

    group = json.loads(
        group_result.stdout
    )

    group_id = group["id"]

    faris_result = run_cli(
        "member-add",
        group_id,
        "Faris",
        "--json",
    )

    assert faris_result.returncode == 0

    faris = json.loads(
        faris_result.stdout
    )

    ada_result = run_cli(
        "member-add",
        group_id,
        "Ada",
        "--json",
    )

    assert ada_result.returncode == 0

    ada = json.loads(
        ada_result.stdout
    )

    expense_result = run_cli(
        "expense-add",
        group_id,
        faris["id"],
        "Apartment",
        "90.00",
        "--json",
    )

    assert expense_result.returncode == 0

    balances_result = run_cli(
        "balances",
        group_id,
        "--json",
    )

    assert balances_result.returncode == 0

    balances = json.loads(
        balances_result.stdout
    )

    balances_by_name = {
        item["member_name"]:
            item["balance_cents"]
        for item in balances
    }

    assert balances_by_name == {
        "Faris": 4500,
        "Ada": -4500,
    }

    assert sum(
        balances_by_name.values()
    ) == 0

    settlements_result = run_cli(
        "settlements",
        group_id,
        "--json",
    )

    assert settlements_result.returncode == 0

    settlements = json.loads(
        settlements_result.stdout
    )

    assert settlements == [
        {
            "from_member_id": ada["id"],
            "from_member_name": "Ada",
            "to_member_id": faris["id"],
            "to_member_name": "Faris",
            "amount_cents": 4500,
        }
    ]