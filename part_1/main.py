import csv
from itertools import islice
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class Transaction:
    """Object representing a single transaction between two users.

    Keyword arguments:
        `user_from (str)`: a user giving money in a transaction
        `user_to (str)`: a user receiving money in a transaction
        `amount (int)`: amount of money exchanged in a transaction
    """

    def __init__(self, user_from: str, user_to: str, amount: int) -> None:
        self.user_from = user_from
        self.user_to = user_to
        self.amount = amount

    def __str__(self) -> str:
        return f"{self.user_from} - {self.user_to} - {self.amount}"


def load_transactions(input_path: str) -> list[Transaction]:
    """Loads a .csv file containing transactions into a list of `Transaction` objects

    Args:
        `input_path (str):` a path to a .csv input file

    Returns:
        `list[Transaction]:` a list of loaded Transaction objects
    """
    with open(input_path) as f:
        reader = csv.reader(f)
        transactions = list(reader)

    transaction_list: list[Transaction] = [
        Transaction(user_from, user_to, int(amount))
        for (user_from, user_to, amount) in transactions
    ]

    return transaction_list


def calculate_balance(transaction_list: list[Transaction]) -> dict[str, int]:
    """Calculate total balance for each user from a list of smaller transactions

    Args:
        `transaction_list (list[Transaction]):` a list of transactions

    Returns:
        `dict[str, int]:` a dictionary containing pairs of user - balance
    """
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
    """Calculate simplified transactions based on total balance of each user

    Args:
        `balance_dict (dict[str, int]):` a dictionary containing pairs of user - balance

    Returns:
        `list[Transaction]:` a list of simplified transactions
    """
    transactions: list[Transaction] = []
    if balance_dict:
        for i, (curr_name, curr_amount) in islice(
            enumerate(balance_dict.items()), 0, len(balance_dict) - 1
        ):
            for name, amount in islice(balance_dict.items(), i + 1, len(balance_dict)):
                if curr_amount * amount < 0:
                    if curr_amount < amount:
                        transactions.append(
                            Transaction(curr_name, name, abs(curr_amount))
                        )
                    else:
                        transactions.append(
                            Transaction(name, curr_name, abs(curr_amount))
                        )
                    balance_dict[name] += curr_amount
                    break

    return transactions


def save_transactions(transactions: list[Transaction], output_path: str) -> None:
    """Save a list of transactions into a .csv file. If a file does not exist, create a new one.

    Args:
        `transactions (list[Transaction]):` a list of transactions
        `output_path (str):` A path to a .csv file to store the transactions
    """
    with open(output_path, "w") as f:
        writer = csv.writer(f)
        for transaction in transactions:
            writer.writerow(
                [transaction.user_from, transaction.user_to, str(transaction.amount)]
            )


def main():
    parser: ArgumentParser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "input_filename", help="A path to a .csv file containing input transactions"
    )
    parser.add_argument(
        "output_filename",
        help="A path to a .csv file, where the output transactions are supposed to be stored",
    )

    args = parser.parse_args()

    transactions = load_transactions(args.input_filename)
    balance = calculate_balance(transactions)

    new_transactions = calculate_transactions(balance)
    save_transactions(new_transactions, args.output_filename)


if __name__ == "__main__":
    main()
