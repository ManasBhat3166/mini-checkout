# Test Plan - Mini Checkout

**Scope:** `index.html` in desktop Chromium. Out of scope: payments, backend, accessibility audit, other browsers/devices.

## Risks, prioritised
| # | Risk | Impact | Likelihood | Covered by |
|---|---|---|---|---|
| 1 | Duplicate order from double-click | High (customer charged/ordered twice) | Medium | AUTO-5, MAN-2 |
| 2 | Wrong total shown / calculated | High (trust, revenue) | Medium | AUTO-3 |
| 3 | Checkout allowed with empty cart | High (empty order) | Medium | AUTO-4, MAN-1 |
| 4 | Checkout allowed with blank required field | Medium-High | Medium | AUTO-2 |
| 5 | Input lost after validation error | Medium (frustration) | Medium | AUTO-2, AUTO-4 |
| 6 | No/unclear confirmation or reference | Medium | Low | AUTO-1 |
| 7 | Odd quantities (0, negative, blank, >99) | Medium | Medium | Exploratory (see below) |

## Automated cases (`tests/test_checkout.py`)
| ID | Test | Steps | Expected (customer-visible) |
|---|---|---|---|
| AUTO-1 | Successful checkout | Add Widget → name "Asha Patel" → Place Order | Confirmation visible with name, ref matching `ORD-[A-Z0-9]{8}`, total $12.50 |
| AUTO-2 | Missing field blocks | Add Gadget, qty 2, name = spaces → Place Order | Message "Please enter your full name."; no confirmation; qty still 2; total $16.00 |
| AUTO-3 | Quantity updates exact total | Widget qty 3 → Gadget qty 2 → remove Widget | Lines $37.50 / $16.00; total $37.50 → $53.50 → $16.00 |
| AUTO-4 (bonus) | Empty cart blocks | Name only → Place Order | "cart is empty" message; no confirmation; name preserved |
| AUTO-5 (bonus) | Double-click | Add Widget, name, dblclick Place Order | Exactly 1 confirmation, 1 reference |

## Manual cases
| ID | Steps | Expected | Actual |
|---|---|---|---|
| MAN-1 Empty cart | Name filled, cart empty, click Place Order | Blocked, clear message, name kept | **As expected** (evidence/M1_empty_cart.png) |
| MAN-2 Rapid double-click | Add item, name, double-click Place Order; then 10 forced re-clicks (button re-enabled via console) | One confirmation; reference never changes | **As expected**: 1 confirmation; ref unchanged (evidence/M2_double_click.png) |

Note: the manual scenarios were executed in a real Chromium via `tests/manual_exploratory.py` (scripted clicks at zero delay, which is faster than a human), and the steps are written so a person can repeat them by hand.

## Exploratory ideas not yet executed (follow-ups)
Quantity 0 / negative / blank / 100+ typed into the field; pasting HTML into the name; "Start new order" resets everything; Firefox/WebKit; keyboard-only flow (Enter on Place Order); mobile viewport.
