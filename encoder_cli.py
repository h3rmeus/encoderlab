#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from encoder_engine import ALGORITHMS, CATEGORIES, encode, decode

R  = "\033[0m"
B  = "\033[1m"
CY = "\033[96m"
GR = "\033[92m"
YL = "\033[93m"
RD = "\033[91m"
DM = "\033[2m\033[90m"

def clr():
    os.system("cls" if os.name == "nt" else "clear")

def algo_menu():
    idx = 1
    mp = {}
    for cat, algos in CATEGORIES.items():
        print(f"  {YL}{cat}{R}")
        for a in algos:
            print(f"    {CY}{idx:2}.{R}  {a}")
            mp[idx] = a
            idx += 1
        print()
    return mp

def pick_algo():
    mp = algo_menu()
    total = len(mp)
    while True:
        ch = input(f"  {CY}>{R}  Number (1-{total}) or q to quit: ").strip()
        if ch.lower() == 'q':
            return None
        try:
            n = int(ch)
            if n in mp:
                return mp[n]
            print(f"  {RD}No such number.{R}")
        except ValueError:
            print(f"  {RD}Please enter a number.{R}")

def get_text(prompt):
    print(f"  {CY}>{R}  {prompt}")
    print(f"  {DM}(empty line finishes input){R}")
    lines = []
    while True:
        try:
            line = input("  ")
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

def print_result(label, text, color):
    print(f"\n  {B}{label}{R}")
    print(f"  {'─'*56}")
    chunk = 70
    for i in range(0, len(text), chunk):
        print(f"  {color}{text[i:i+chunk]}{R}")
    print(f"  {'─'*56}")

def session():
    clr()

    algo = pick_algo()
    if algo is None:
        return False

    print(f"\n  {GR}✔{R}  {B}{algo}{R}")
    print(f"  {DM}{ALGORITHMS[algo]['desc']}{R}")
    print(f"  {'─'*56}")

    print(f"\n  {B}OPERATION:{R}")
    print(f"    {CY}1.{R}  Encode")
    print(f"    {CY}2.{R}  Decode")
    op = input(f"  {CY}>{R}  Choice: ").strip()
    if op not in ("1", "2"):
        print(f"  {RD}Invalid choice.{R}")
        return True

    prompt = "Enter text to encode:" if op == "1" else "Enter encoded text to decode:"
    text = get_text(prompt)
    if not text.strip():
        print(f"  {YL}Empty input.{R}")
        return True

    try:
        if op == "1":
            result = encode(algo, text)
            print_result("ENCODED RESULT:", result, CY)
        else:
            result = decode(algo, text)
            print_result("DECODED RESULT:", result, GR)
        print(f"  {GR}✅ Done!{R}")
    except Exception as e:
        print(f"\n  {RD}❌ Error: {e}{R}")
        print(f"  {DM}Make sure the text matches the selected algorithm.{R}")

    return True

def main():
    while True:
        try:
            if not session():
                break
            again = input(f"\n  {CY}>{R}  Run again? [y/n]: ").strip().lower()
            if again not in ("y", "yes", ""):
                break
        except KeyboardInterrupt:
            print(f"\n\n  {YL}Interrupted.{R}")
            break
    print(f"\n  {CY}Goodbye! 👋{R}\n")

if __name__ == "__main__":
    main()
