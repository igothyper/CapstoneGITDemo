#!/usr/bin/env python3
# Added analytics tracker
"""A tiny tracker for my tech watchlist. Prices are made up, not live quotes."""

import json
from decimal import Decimal, InvalidOperation
from pathlib import Path


def load_watchlist():
    path = Path(__file__).with_name("data.json")
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    prices = data["prices"]
    if not prices:
        raise ValueError("The mock watchlist is empty.")
    for item in prices.values():
        price = Decimal(str(item["price"]))
        if not price.is_finite() or price <= 0:
            raise ValueError("Mock prices must be positive, finite numbers.")
    return data


def collect_holdings(prices):
    holdings = {}
    print("Enter TICKER SHARES (example: QQQ 2.5). Type done to finish.")
    print("Repeated tickers add shares; fractional shares are welcome.\n")
    while True:
        entry = input("holding> ").strip()
        if entry.lower() == "done":
            return holdings
        parts = entry.upper().split()
        if len(parts) != 2:
            print("Try a ticker and share count, like NVDA 3.")
            continue
        ticker, raw_shares = parts
        if ticker not in prices:
            print("That ticker isn't in the mock watchlist.")
            continue
        try:
            shares = Decimal(raw_shares)
        except InvalidOperation:
            print("Shares must be a number.")
            continue
        if not shares.is_finite() or shares <= 0:
            print("Use a positive, finite share count.")
            continue
        holdings[ticker] = holdings.get(ticker, Decimal("0")) + shares


def print_report(holdings, prices):
    if not holdings:
        print("No holdings entered. Watchlist saved for another day.")
        return
    values = {
        ticker: shares * Decimal(str(prices[ticker]["price"]))
        for ticker, shares in holdings.items()
    }
    total = sum(values.values(), Decimal("0"))
    print("\nMY TECH / AI CORNER")
    print(f"{'Ticker':<8} {'Shares':>12} {'Mock price':>14} {'Value':>14}")
    print("-" * 51)
    for ticker in sorted(holdings):
        price = Decimal(str(prices[ticker]["price"]))
        print(f"{ticker:<8} {holdings[ticker]:>12,.4f} "
              f"${price:>13,.2f} ${values[ticker]:>13,.2f}")
    print(f"\nMock portfolio total: ${total:,.2f}")
    # TODO: show the largest position and its portfolio weight.
    print("Share quantities displayed to 4 decimals; totals use full input precision.")
    print("Practice snapshot only. No live prices, fees, or investment advice.")


def main():
    try:
        data = load_watchlist()
        print("Tech & AI ETF Portfolio Tracker")
        print(f"Price set: {data['snapshot']} | Currency: {data['currency']}")
        for ticker, item in sorted(data["prices"].items()):
            print(f"  {ticker:<6} {item['name']}")
        print()
        print_report(collect_holdings(data["prices"]), data["prices"])
    except (OSError, ValueError, KeyError, TypeError, InvalidOperation) as error:
        raise SystemExit(f"Couldn't read the mock watchlist: {error}") from error
    except (EOFError, KeyboardInterrupt):
        print("\nTracker closed.")


if __name__ == "__main__":
    main()
