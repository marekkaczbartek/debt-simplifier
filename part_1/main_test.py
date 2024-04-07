import pytest
from main import (
    Transaction,
    load_transactions,
    calculate_balance,
    calculate_transactions,
)


debts_1_path: str = (
    "/home/bartek/projects/ocado-cloud-recruitment/test_data/debts_1.csv"
)
debts_3_path: str = (
    "/home/bartek/projects/ocado-cloud-recruitment/test_data/debts_3.csv"
)
debts_empty_path: str = (
    "/home/bartek/projects/ocado-cloud-recruitment/test_data/debts_empty.csv"
)
debts_incorrect_format_path: str = (
    "/home/bartek/projects/ocado-cloud-recruitment/test_data/debts_incorrect_format.csv"
)


def assert_lists_equal(expected, actual):
    assert len(expected) == len(actual)
    assert all([str(a) == str(e)] for a, e in zip(expected, actual))


def test_load_transactions():
    expected_transactions: list[Transaction] = [
        Transaction("Mark", "Jessica", 12),
        Transaction("Manny", "Jessica", 18),
        Transaction("Mark", "Manny", 200),
        Transaction("Jessica", "Mark", 230),
    ]

    transactions: list[Transaction] = load_transactions(debts_3_path)

    assert_lists_equal(expected_transactions, transactions)


def test_load_transactions_empty():
    transactions: list[Transaction] = load_transactions(debts_empty_path)
    assert not transactions


def test_load_transactions_incorrect_format():
    expected_transactions: list[Transaction] = [
        Transaction("Mark", "Jessica", 12),
        Transaction("Manny", "Jessica", 18),
        Transaction("Jessica", "Mark", 230),
    ]
    transactions: list[Transaction] = load_transactions(debts_incorrect_format_path)
    assert_lists_equal(expected_transactions, transactions)


def test_calculate_balance():
    transactions: list[Transaction] = [
        Transaction("Mark", "Jessica", 12),
        Transaction("Manny", "Jessica", 18),
        Transaction("Mark", "Manny", 200),
        Transaction("Jessica", "Mark", 230),
    ]
    expected_balance_dict: dict[str, int] = {
        "Mark": -18,
        "Jessica": 200,
        "Manny": -182,
    }

    balance_dict = calculate_balance(transactions)

    assert balance_dict == expected_balance_dict


def test_calculate_balance_empty():
    balance_dict = calculate_balance([])

    assert not balance_dict


def test_calculate_transactions():
    balance: dict[str, int] = {
        "Mark": -18,
        "Jessica": 200,
        "Manny": -182,
    }

    expected_transactions: list[Transaction] = [
        Transaction("Mark", "Jessica", 18),
        Transaction("Manny", "Jessica", 182),
    ]

    transactions: list[Transaction] = calculate_transactions(balance)

    assert_lists_equal(expected_transactions, transactions)


def test_calculate_transactions_empty():
    transactions: list[Transaction] = calculate_transactions({})

    assert not transactions
