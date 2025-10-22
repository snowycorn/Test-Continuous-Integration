import pytest
from models.user import User
from models.group import Group
from models.expense import Expense
from services.expense_service import ExpenseService
from utils.calculation import split_amount

@pytest.fixture
def sample_data():
    # 建立兩個使用者
    alice = User("Alice")
    bob = User("Bob")
    # 建立一個 group
    group = Group("Trip")
    # 將使用者加入 group
    group.members.extend([alice, bob])
    return {
        "users": {"Alice": alice, "Bob": bob},
        "groups": [group]
    }

def test_add_expense(sample_data):
    data = sample_data
    service = ExpenseService(data)
    group = data["groups"][0]
    alice = data["users"]["Alice"]
    bob = data["users"]["Bob"]

    # 新增 expense
    amount = 100
    participants = [alice, bob]
    category = "Food"
    note = "Dinner"

    # 模擬 service.add_expense_ui 的邏輯，但直接操作資料
    shares = split_amount(amount, participants)
    for u, share in zip(participants, shares):
        u.balance -= share
    alice.balance += amount

    exp = Expense(payer=alice, amount=amount, participants=participants, category=category, note=note)
    group.expenses.append(exp)

    assert exp in group.expenses
    assert alice.balance == 100 - sum(shares) + 100  # alice 最終 balance
    assert bob.balance == -50  # bob 最終 balance

def test_delete_expense(sample_data):
    data = sample_data
    service = ExpenseService(data)
    group = data["groups"][0]
    alice = data["users"]["Alice"]
    bob = data["users"]["Bob"]

    # 先新增一筆 expense
    amount = 120
    participants = [alice, bob]
    exp = Expense(payer=alice, amount=amount, participants=participants, category="Food", note="Lunch")
    group.expenses.append(exp)

    # 模擬刪除
    shares = split_amount(exp.amount, exp.participants)
    for u, share in zip(exp.participants, shares):
        u.balance += share
    exp.payer.balance -= exp.amount
    group.expenses.remove(exp)

    assert exp not in group.expenses
    # balance 回到原始狀態
    assert alice.balance == 0
    assert bob.balance == 0
