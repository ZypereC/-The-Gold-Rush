import time

class Graphing:
    def __init__(self):
        self.balance = 0
        self.history = []
        self.record_history("Graphing account created")

    def record_history(self, transaction):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.history.append((timestamp, transaction, self.balance))

    def deposit(self, balance):
        if balance > 0:
            self.balance += balance
            self.record_history(f"Deposited ${balance:.2f}")
            print(f"Successfully deposited ${balance:.2f}. New balance: ${self.balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, balance):
        if 0 < balance <= self.balance:
            self.balance -= balance
            self.record_history(f"Withdrew ${balance:.2f}")
            print(f"Successfully withdrew ${balance:.2f}. New balance: ${self.balance:.2f}")
        else:
            print("Withdrawal amount must be positive and less than or equal to the balance.")

    def Build_graph(self):
        if not self.history:
            print("No transaction history available to build a graph.")
        else:
            print("\n--- Transaction History ---")
            for timestamp, transaction, balance in self.history:
                print(f"{timestamp} - {transaction} - Balance: ${balance:.2f}")


# Only runs if Finances.py is executed directly, not when imported
if __name__ == "__main__":
    account = Graphing()

    Account_options = {
        '1': 'Deposit',
        '2': 'Withdraw',
        '3': 'View Balance',
        '4': 'Transaction history',
        '5': 'Exit'
    }

    while True:
        print("\nOptions:")
        for k, v in Account_options.items():
            print(f"{k}: {v}")

        User_input = input("Choose an option (1-5): ").strip()
        if User_input == '1':
            amount = float(input("Enter deposit amount: "))
            account.deposit(amount)
        elif User_input == '2':
            amount = float(input("Enter withdrawal amount: "))
            account.withdraw(amount)
        elif User_input == '3':
            print(f"Current balance: ${account.balance:.2f}")
        elif User_input == '4':
            account.Build_graph()
        elif User_input == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
