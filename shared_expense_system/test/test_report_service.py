import pytest
from models.user import User
from models.group import Group
from models.expense import Expense
from services.report_service import ReportService

def test_report_balances():
    alice = User("Alice")
    bob = User("Bob")
    group = Group("Trip")
    group.members = [alice, bob]

    exp1 = Expense(alice, 100, [alice, bob])
    exp2 = Expense(bob, 50, [alice, bob])
    group.expenses = [exp1, exp2]

    # 模擬分攤
    from utils.calculation import split_amount
    for e in group.expenses:
        shares = split_amount(e.amount, e.participants)
        for u, share in zip(e.participants, shares):
            u.balance -= share
        e.payer.balance += e.amount

    report_service = ReportService({"users": {"Alice": alice, "Bob": bob}, "groups": [group]})
    # 簡單檢查總和
    total_balance = sum(u.balance for u in group.members)
    assert round(total_balance, 2) == 0.0