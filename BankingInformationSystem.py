import pandas as pd
import numpy as np
import os
from datetime import datetime

file = "accounts.csv"

# Create file if not exists
if not os.path.exists(file):
    df = pd.DataFrame(columns=["Name", "PIN", "Balance"])
    df.to_csv(file, index=False)

# -------- Account Creation --------
def create_account():
    name = input("Enter name: ").strip()
    pin = input("Set PIN: ").strip()
    balance = int(input("Enter initial balance: "))

    df = pd.read_csv(file, dtype=str)

    # Check duplicate
    if name in df["Name"].values:
        print("User already exists!")
        return

    new_user = pd.DataFrame([[name, pin, str(balance)]], columns=["Name", "PIN", "Balance"])

    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(file, index=False)

    print("Account created successfully!")
# -------- Login --------
def login():
    name = input("Enter name: ").strip()
    pin = input("Enter PIN: ").strip()

    df = pd.read_csv(file, dtype=str)   # Force everything as string

    # Clean data properly
    df["Name"] = df["Name"].str.strip()
    df["PIN"] = df["PIN"].str.strip()

    for i in range(len(df)):
        if df.loc[i, "Name"] == name and df.loc[i, "PIN"] == pin:
            print("Login successful!")
            return name

    print("Invalid credentials")
    return None

# -------- Banking System --------
def banking_system(user):
    history = []

    while True:
        print("\n===== Banking Menu =====")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Mini Statement")
        print("6. Exit")

        try:
            choice = int(input("Enter choice: "))
        except:
            print("Invalid input")
            continue

        df = pd.read_csv(file)
        index = df[df["Name"] == user].index[0]

        if choice == 1:
            amt = np.int64(input("Enter deposit amount: "))
            if amt <= 0:
                print("Invalid amount")
            else:
                df.at[index, "Balance"] += amt
                time = datetime.now()
                history.append(f"Deposited {amt} at {time}")
                print("Deposited:", amt)
                print("Total Balance:", df.at[index, "Balance"])

        elif choice == 2:
            amt = np.int64(input("Enter withdrawal amount: "))
            if amt <= 0:
                print("Invalid amount")
            elif amt > df.at[index, "Balance"]:
                print("Insufficient balance")
            else:
                df.at[index, "Balance"] -= amt
                time = datetime.now()
                history.append(f"Withdrawn {amt} at {time}")
                print("Withdrawn:", amt)
                print("Total Balance:", df.at[index, "Balance"])

        elif choice == 3:
            print("Current Balance:", df.at[index, "Balance"])

        elif choice == 4:
            print("\nTransaction History:")
            if not history:
                print("No transactions yet")
            else:
                for h in history:
                    print(h)

        elif choice == 5:
            print("\nMini Statement (Last 3):")
            for h in history[-3:]:
                print(h)

        elif choice == 6:
            print("Exiting...")
            break

        else:
            print("Invalid choice")

        df.to_csv(file, index=False)

# -------- Main Menu --------
while True:
    print("\n===== Main Menu =====")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    try:
        ch = int(input("Enter choice: "))
    except:
        print("Invalid input")
        continue

    if ch == 1:
        create_account()

    elif ch == 2:
        user = login()
        if user:
            banking_system(user)

    elif ch == 3:
        print("Thank you!")
        break

    else:
        print("Invalid choice")