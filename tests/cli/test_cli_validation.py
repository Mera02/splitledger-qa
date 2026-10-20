import json


def create_group(run_cli, name):
    result = run_cli(
        "group-create",
        name,
        "--json",
    )

    assert result.returncode == 0

    return json.loads(result.stdout)


def add_member(run_cli, group_id, name):
    result = run_cli(
        "member-add",
        group_id,
        name,
        "--json",
    )

    assert result.returncode == 0

    return json.loads(result.stdout)


def test_cli_rejects_negative_amount(run_cli):
    group = create_group(
        run_cli,
        "Negative Amount Test",
    )

    faris = add_member(
        run_cli,
        group["id"],
        "Faris",
    )

    result = run_cli(
        "expense-add",
        group["id"],
        faris["id"],
        "Invalid expense",
        "--json",
        "--",
        "-10.00",
    )

    assert result.returncode == 1

    assert json.loads(result.stdout) == {
        "error":
            "Amount must be greater than zero."
    }


def test_cli_rejects_duplicate_member(run_cli):
    group = create_group(
        run_cli,
        "Duplicate Member Test",
    )

    add_member(
        run_cli,
        group["id"],
        "Faris",
    )

    result = run_cli(
        "member-add",
        group["id"],
        "  FARIS  ",
        "--json",
    )

    assert result.returncode == 1

    assert json.loads(result.stdout) == {
        "error":
            "Member already exists in this group."
    }


def test_cli_rejects_payer_from_other_group(
    run_cli,
):
    first_group = create_group(
        run_cli,
        "First Group",
    )

    second_group = create_group(
        run_cli,
        "Second Group",
    )

    add_member(
        run_cli,
        first_group["id"],
        "Faris",
    )

    outside_member = add_member(
        run_cli,
        second_group["id"],
        "Ada",
    )

    result = run_cli(
        "expense-add",
        first_group["id"],
        outside_member["id"],
        "Invalid payer",
        "20.00",
        "--json",
    )

    assert result.returncode == 1

    assert json.loads(result.stdout) == {
        "error":
            "Payer must belong to the group."
    }