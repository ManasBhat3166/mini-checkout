"""Scripted run of the two MANUAL scenarios so observations + screenshots are reproducible."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
URL = (ROOT / "index.html").as_uri()
EV = ROOT / "evidence"

with sync_playwright() as p:
    b = p.chromium.launch()

    # M1: empty cart
    pg = b.new_context().new_page(); pg.goto(URL)
    pg.get_by_label("Full name (required)").fill("Asha Patel")
    pg.get_by_role("button", name="Place Order").click()
    print("M1 cart-error      :", pg.get_by_test_id("cart-error").inner_text())
    print("M1 confirmation vis:", pg.get_by_test_id("confirmation").is_visible())
    print("M1 name preserved  :", pg.get_by_label("Full name (required)").input_value())
    pg.screenshot(path=str(EV / "M1_empty_cart.png"))

    # M2: rapid double-click, then 10 forced clicks after success
    pg = b.new_context().new_page(); pg.goto(URL)
    pg.get_by_test_id("add-widget").click()
    pg.get_by_label("Full name (required)").fill("Asha Patel")
    pg.get_by_role("button", name="Place Order").dblclick(delay=0)
    pg.get_by_test_id("confirmation").wait_for()
    first_ref = pg.get_by_test_id("order-ref").inner_text()
    pg.evaluate("document.getElementById('place-order').disabled=false; for(let i=0;i<10;i++) document.getElementById('place-order').click()")
    print("M2 confirmations   :", pg.get_by_test_id("confirmation").count())
    print("M2 ref unchanged after 10 forced clicks:", first_ref == pg.get_by_test_id("order-ref").inner_text(), first_ref)
    pg.screenshot(path=str(EV / "M2_double_click.png"))
    b.close()
