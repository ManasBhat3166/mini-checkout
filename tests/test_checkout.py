"""Browser tests for the Mini Checkout page (pytest + Playwright).

Each test gets a brand-new browser context (no cookies/storage) and a fresh
page load, so every check starts from a clean state. Assertions use
Playwright's auto-retrying `expect`, i.e. they wait for what the customer
sees rather than using fixed sleeps.
"""
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect, sync_playwright

URL = (Path(__file__).resolve().parent.parent / "index.html").as_uri()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture()
def page(browser) -> Page:
    ctx = browser.new_context()          # clean state for every test
    pg = ctx.new_page()
    pg.goto(URL)
    expect(pg.get_by_test_id("order-total")).to_have_text("$0.00")
    yield pg
    ctx.close()


def test_successful_checkout_shows_confirmation(page: Page):
    page.get_by_test_id("add-widget").click()
    page.get_by_label("Full name (required)").fill("Asha Patel")
    page.get_by_role("button", name="Place Order").click()

    confirmation = page.get_by_test_id("confirmation")
    expect(confirmation).to_be_visible()
    expect(confirmation).to_contain_text("Asha Patel")
    expect(page.get_by_test_id("order-ref")).to_have_text(re.compile(r"^ORD-[A-Z0-9]{8}$"))
    expect(page.get_by_test_id("conf-total")).to_have_text("$12.50")


def test_missing_name_blocks_checkout_and_keeps_cart(page: Page):
    page.get_by_test_id("add-gadget").click()
    page.get_by_test_id("qty-gadget").fill("2")
    page.get_by_test_id("qty-gadget").press("Tab")
    page.get_by_label("Full name (required)").fill("   ")   # whitespace only = blank
    page.get_by_role("button", name="Place Order").click()

    expect(page.get_by_test_id("name-error")).to_have_text("Please enter your full name.")
    expect(page.get_by_test_id("confirmation")).to_be_hidden()
    # customer's input is preserved
    expect(page.get_by_test_id("qty-gadget")).to_have_value("2")
    expect(page.get_by_test_id("order-total")).to_have_text("$16.00")


def test_quantity_change_updates_exact_total(page: Page):
    page.get_by_test_id("add-widget").click()
    page.get_by_test_id("qty-widget").fill("3")
    page.get_by_test_id("qty-widget").press("Tab")
    expect(page.get_by_test_id("line-widget")).to_have_text("$37.50")
    expect(page.get_by_test_id("order-total")).to_have_text("$37.50")

    page.get_by_test_id("add-gadget").click()
    page.get_by_role("button", name="Increase Gadget").click()   # gadget qty 2
    expect(page.get_by_test_id("line-gadget")).to_have_text("$16.00")
    expect(page.get_by_test_id("order-total")).to_have_text("$53.50")

    page.get_by_test_id("remove-widget").click()
    expect(page.get_by_test_id("order-total")).to_have_text("$16.00")


# ---- bonus checks for the two manual-test risks ----
def test_empty_cart_blocks_checkout(page: Page):
    page.get_by_label("Full name (required)").fill("Asha Patel")
    page.get_by_role("button", name="Place Order").click()
    expect(page.get_by_test_id("cart-error")).to_contain_text("cart is empty")
    expect(page.get_by_test_id("confirmation")).to_be_hidden()
    expect(page.get_by_label("Full name (required)")).to_have_value("Asha Patel")


def test_double_click_place_order_gives_single_confirmation(page: Page):
    page.get_by_test_id("add-widget").click()
    page.get_by_label("Full name (required)").fill("Asha Patel")
    page.get_by_role("button", name="Place Order").dblclick(delay=0)
    expect(page.get_by_test_id("confirmation")).to_have_count(1)
    expect(page.get_by_test_id("order-ref")).to_have_count(1)
