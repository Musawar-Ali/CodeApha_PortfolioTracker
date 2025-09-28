"""
stock_tracker.py
Simple stock portfolio tracker using a hardcoded price dictionary.

Usage examples:
    python stock_tracker.py              # interactive input
    python stock_tracker.py --save csv   # saves to portfolio.csv
Author: Musawar Ali 
"""

# Paste your original tracker code here

import csv
import argparse
from datetime import datetime
import os # Import the os module

# Hardcoded sample prices (can be adjusted)
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 125.00,
    "MSFT": 300.00,
    "AMZN": 100.00,
    "NFLX": 350.00
}

def ask_portfolio():
    print("Available tickers (sample):", ", ".join(sorted(STOCK_PRICES.keys())))
    print("Type 'done' when finished.")
    entries = []
    while True:
        ticker = input("Ticker (e.g., AAPL): ").strip().upper()
        if ticker == "DONE" or ticker == "":
            break
        qty_raw = input("Quantity (integer): ").strip()
        try:
            qty = int(qty_raw)
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("Enter a positive integer for quantity.")
            continue
        # If ticker unknown, offer to use a price or add custom price
        if ticker not in STOCK_PRICES:
            print("Ticker not in predefined prices.")
            while True:
                choice = input("Enter custom price for {} or type 'skip' to skip: ".format(ticker)).strip().lower()
                if choice == "skip":
                    price = None
                    break
                try:
                    price = float(choice)
                    break
                except ValueError:
                    print("Enter a numeric price or 'skip'.")
            if price is None:
                print("Skipping", ticker)
                continue
        else:
            price = STOCK_PRICES[ticker]
        entries.append({"ticker": ticker, "quantity": qty, "price": price})
    return entries

def summarize(entries):
    print("\n--- Portfolio Summary ---")
    total = 0.0
    lines = []
    for e in entries:
        invest = e["quantity"] * e["price"]
        total += invest
        line = f"{e['ticker']:6s} qty={e['quantity']:4d} price={e['price']:8.2f} => value={invest:10.2f}"
        lines.append(line)
        print(line)
    print("-" * 40)
    print(f"Total investment value: {total:.2f}")
    return lines, total

def save_csv(entries, filename="portfolio.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ticker", "quantity", "price", "value"])
        for e in entries:
            writer.writerow([e["ticker"], e["quantity"], f"{e['price']:.2f}", f"{e['quantity']*e['price']:.2f}"])
    print(f"Saved CSV to {filename}")

def save_txt(lines, total, filename="portfolio.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Portfolio Summary\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        for l in lines:
            f.write(l + "\n")
        f.write("\n")
        f.write(f"Total: {total:.2f}\n")
    print(f"Saved TXT to {filename}")

def main(save=None):
    entries = ask_portfolio()
    if not entries:
        print("No entries provided. Exiting.")
        return
    lines, total = summarize(entries)
    if save == "csv" or save == "both":
        save_csv(entries)
    if save == "txt" or save == "both":
        save_txt(lines, total)
