import csv
from itertools import islice
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class Transaction:
    def __init__(self, user_from: str, user_to: str, amount: int) -> None:
        self.user_from = user_from
        self.user_to = user_to
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.user_from} - {self.user_to} - {self.amount}"


def load_transactions(absolute_path: str) -> list[Transaction]:
    with open(absolute_path) as f:
        reader = csv.reader(f)
        transactions = list(reader)

    transaction_list: list[Transaction] = []

    for transaction in transactions:
        user_from, user_to, amount = transaction
        transaction_list.append(Transaction(user_from, user_to, int(amount)))

    return transaction_list


def calculate_balance(transaction_list: list[Transaction]) -> dict[str, int]:
    balance_dict: dict[str, int] = {}
    for transaction in transaction_list:
        if transaction.user_from not in balance_dict:
            balance_dict[transaction.user_from] = 0
        if transaction.user_to not in balance_dict:
            balance_dict[transaction.user_to] = 0

        balance_dict[transaction.user_from] += transaction.amount
        balance_dict[transaction.user_to] -= transaction.amount

    return balance_dict


def calculate_transactions(balance_dict: dict[str, int]) -> list[Transaction]:
    transactions: list[Transaction] = []
    for i, (name, amount) in islice(
        enumerate(balance_dict.items()), 0, len(balance_dict) - 1
    ):
        for n in islice(balance_dict, i + 1, len(balance_dict)):
            a = balance_dict[n]
            if amount * a < 0:
                if amount < a:
                    transactions.append(Transaction(name, n, abs(amount)))
                else:
                    transactions.append(Transaction(n, name, abs(amount)))
                balance_dict[n] += amount
                break
    return transactions


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "filename",
    )

    filename = parser.parse_args().filename
    # filename = "/home/bartek/projects/ocado-cloud-recruitment/test_data/debts_1.csv"

    transactions = load_transactions(filename)
    balance = calculate_balance(transactions)
    new_transactions = calculate_transactions(balance)
    for t in new_transactions:
        print(t)
