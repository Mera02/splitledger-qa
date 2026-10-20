from playwright.sync_api import Page, expect


FRONTEND_URL = "http://localhost:5173"


def test_splitledger_ui_loads(page: Page):
    page.goto(FRONTEND_URL)

    expect(
        page.get_by_role(
            "heading",
            name="SplitLedger",
        )
    ).to_be_visible()

    expect(
        page.get_by_role(
            "button",
            name="+ New group",
        )
    ).to_be_visible()

    expect(
        page.get_by_role(
            "heading",
            name="Members",
        )
    ).to_be_visible()

    expect(
        page.get_by_role(
            "heading",
            name="Add expense",
        )
    ).to_be_visible()