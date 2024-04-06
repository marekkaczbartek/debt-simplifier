import csv
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
        data = list(reader)

    transaction_list: list[Transaction] = []

    for entry in data:
        transaction_list.append(Transaction(entry[0], entry[1], int(entry[2])))

    return transaction_list


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "filename",
    )

    filename = parser.parse_args().filename

    transactions = load_transactions(filename)
    for t in transactions:
        print(t)
