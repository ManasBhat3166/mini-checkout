# Results

**Environment:** Python 3.12, Playwright 1.63, Chromium 157 (headless), Linux, page loaded via `file://`.

## Automated (`python3 -m pytest tests -v`) - 5 passed, 0 failed (2.13 s)
```
test_successful_checkout_shows_confirmation .............. PASSED
test_missing_name_blocks_checkout_and_keeps_cart ......... PASSED
test_quantity_change_updates_exact_total ................. PASSED
test_empty_cart_blocks_checkout .......................... PASSED
test_double_click_place_order_gives_single_confirmation .. PASSED
```
Raw output: `evidence/pytest_output.txt`

## Manual / exploratory (`evidence/manual_output.txt`)
```
M1 cart-error      : Your cart is empty. Add at least one item before placing an order.
M1 confirmation vis: False
M1 name preserved  : Asha Patel
M2 confirmations   : 1
M2 ref unchanged after 10 forced clicks: True ORD-BT5YU8IM
```
Screenshots: `evidence/M1_empty_cart.png`, `evidence/M2_double_click.png`

## Defects
**None found** in the scenarios tested. No defect has been invented for this report.

## Observations / limitations (not defects)
- Order references combine a timestamp and a random suffix; with no backend, uniqueness across customers cannot be guaranteed (a server would issue real IDs).
- Only Chromium was tested; the exploratory ideas in TEST_PLAN.md remain unexecuted.
- The tests' `dblclick` runs at machine speed, which is a harsher timing than a human double-click.
