from uuid import uuid4

from playwright.sync_api import Page, expect


FRONTEND_URL = "http://localhost:5173"


def test_complete_expense_flow_through_ui(page: Page):
    group_name = f"UI QA Trip {uuid4().hex[:8]}"

    page.goto(FRONTEND_URL)

    # Create group
    page.get_by_role(
        "button",
        name="+ New group",
    ).click()

    page.get_by_placeholder(
        "Group name"
    ).fill(group_name)

    page.get_by_role(
        "button",
        name="Create",
        exact=True,
    ).click()

    expect(
        page.get_by_role(
            "heading",
            name=group_name,
        )
    ).to_be_visible()

    # Scope the Members section
    members_section = page.locator(
        "section"
    ).filter(
        has=page.get_by_role(
            "heading",
            name="Members",
        )
    )

    # Add Faris
    page.get_by_role(
        "button",
        name="+ Add member",
    ).click()

    page.get_by_placeholder(
        "Member name"
    ).fill("Faris")

    page.get_by_role(
        "button",
        name="Add",
        exact=True,
    ).click()

    expect(
        members_section.get_by_text(
            "Faris",
            exact=True,
        )
    ).to_be_visible()

    # Add Ada
    page.get_by_role(
        "button",
        name="+ Add member",
    ).click()

    page.get_by_placeholder(
        "Member name"
    ).fill("Ada")

    page.get_by_role(
        "button",
        name="Add",
        exact=True,
    ).click()

    expect(
        members_section.get_by_text(
            "Ada",
            exact=True,
        )
    ).to_be_visible()

    # Add expense
    page.get_by_label(
        "Description"
    ).fill("Apartment")

    page.get_by_label(
        "Amount"
    ).fill("90.00")

    page.get_by_label(
        "Paid by"
    ).select_option(
        label="Faris"
    )

    page.get_by_role(
        "button",
        name="Add expense",
    ).click()

    # Scope the Expenses section
    expenses_section = page.locator(
        "section"
    ).filter(
        has=page.get_by_role(
            "heading",
            name="Expenses",
        )
    )

    # Verify expense
    expect(
        expenses_section.get_by_text(
            "Apartment",
            exact=True,
        )
    ).to_be_visible()

    expect(
        expenses_section.get_by_text(
            "90.00 KM",
            exact=True,
        )
    ).to_be_visible()

    # Scope the Balances section
    balances_section = page.locator(
        "section"
    ).filter(
        has=page.get_by_role(
            "heading",
            name="Balances",
        )
    )

    # Verify balances
    expect(
        balances_section.get_by_text(
            "+45.00 KM",
            exact=True,
        )
    ).to_be_visible()

    expect(
        balances_section.get_by_text(
            "-45.00 KM",
            exact=True,
        )
    ).to_be_visible()

    # Scope the Settlements section
    settlements_section = page.locator(
        "section"
    ).filter(
        has=page.get_by_role(
            "heading",
            name="Suggested settlements",
        )
    )

    # Verify settlement
    expect(
        settlements_section.get_by_text(
            "Ada → Faris",
            exact=True,
        )
    ).to_be_visible()

    expect(
        settlements_section.get_by_text(
            "45.00 KM",
            exact=True,
        )
    ).to_be_visible()