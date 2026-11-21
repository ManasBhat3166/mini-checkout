# Mini Checkout + Browser Test Suite

A single-page checkout (plain HTML/CSS/JS, no backend, no build step) and a Playwright browser test suite.

## Files
| Path | Purpose |
|---|---|
| `index.html` | The checkout page (open directly in a browser) |
| `tests/test_checkout.py` | Automated browser tests (3 required + 2 bonus) |
| `tests/manual_exploratory.py` | Re-runs the two manual scenarios, prints observations, saves screenshots |
| `TEST_PLAN.md` | Risk-prioritised test plan and manual test log |
| `RESULTS.md` | Actual results of the runs, defects section |
| `evidence/` | Screenshots + raw console output |

## Features
- Two products: **Widget $12.50**, **Gadget $8.00** (prices held as integer cents, so no float rounding errors).
- Add / remove items, `−` / `+` buttons or type a quantity (clamped to 1–99); line totals and order total update instantly.
- Required field: **Full name** (whitespace-only counts as blank).
- Empty cart or blank name blocks checkout with a message next to the problem; nothing the customer entered is cleared.
- Success shows one confirmation with a reference (`ORD-XXXXXXXX`) and total. The page locks synchronously on the first successful submit and disables the button, so double-clicks cannot create a second confirmation.

## Run the app
Open `index.html` in any browser (double-click it), or: `python3 -m http.server 8000` then visit http://localhost:8000.

## Run the browser tests
Requires Python 3.9+.
```bash
pip install pytest playwright
playwright install chromium
python3 -m pytest tests -v
```
Each test launches a fresh browser context and reloads the page, so state never leaks between tests. Assertions use Playwright's auto-retrying `expect(...)` on visible text (no `sleep`/fixed waits).

Optional - re-run the manual scenarios and regenerate screenshots:
```bash
python3 tests/manual_exploratory.py
```

## Manual browser steps (reproduce by hand)
1. **Empty cart:** open page → type a name → click **Place Order**. Expect red "cart is empty" message, no confirmation, name still filled.
2. **Rapid double-click:** add a Widget → type a name → double-click **Place Order** as fast as possible. Expect exactly one confirmation and one reference.
