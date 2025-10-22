import pytest
from models.user import User
from models.group import Group
from models.expense import Expense
from services.expense_service import ExpenseService
from utils.calculation import split_amount

@pytest.fixture
def setup_data():
    # 建立兩個使用者
    alice = User("Alice")
    bob = User("Bob")

    # 建立群組並加入成員
    group = Group("Trip")
    group.members.extend([alice, bob])

    data = {"users": {"Alice": alice, "Bob": bob}, "groups": [group]}
    return data


def test_add_expense_ui(monkeypatch, capsys, setup_data):
    """模擬使用者完整輸入流程: 新增一筆支出"""
    service = ExpenseService(setup_data)
    alice = setup_data["users"]["Alice"]
    bob = setup_data["users"]["Bob"]
    group = setup_data["groups"][0]

    # 模擬輸入流程：
    # 1. 選擇 group (1)
    # 2. 選擇付款人 (1 -> Alice)
    # 3. 選擇參與者 (1,2)
    # 4. 輸入金額 (100)
    # 5. 輸入類別 (Food)
    # 6. 輸入備註 (Dinner)
    inputs = iter([
        "1",      # group
        "1",      # payer: Alice
        "1,2",    # participants: Alice, Bob
        "100",    # amount
        "Food",   # category
        "Dinner"  # note
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # 初始 balances 應為 0
    assert alice.balance == 0
    assert bob.balance == 0

    # 執行 add_expense_ui
    service.add_expense_ui()

    # 擷取輸出內容
    output = capsys.readouterr().out

    # 驗證輸出與邏輯
    assert "Expense added." in output
    assert len(group.expenses) == 1
    exp = group.expenses[0]
    assert exp.amount == 100
    assert exp.category == "Food"
    assert exp.note == "Dinner"
    assert exp.payer.name == "Alice"

    # 計算期望 balance（依現有 split_amount 行為）
    shares = split_amount(100, [alice, bob])
    assert alice.balance == -shares[0] + 100
    assert bob.balance == -shares[1]

def test_delete_expense_ui(monkeypatch, capsys, setup_data):
    """模擬刪除一筆支出"""
    service = ExpenseService(setup_data)
    group = setup_data["groups"][0]
    alice = setup_data["users"]["Alice"]
    bob = setup_data["users"]["Bob"]

    # 先建立一筆支出
    amount = 120
    participants = [alice, bob]
    # 應用 split_amount 行為更新 balance（模擬新增）
    shares = split_amount(amount, participants)
    for u, share in zip(participants, shares):
        u.balance -= share
    alice.balance += amount
    exp = Expense(payer=alice, amount=amount, participants=[alice, bob], category="Food", note="Lunch")
    group.expenses.append(exp)

    assert len(group.expenses) == 1
    assert alice.balance == -shares[0] + 120
    assert bob.balance == -shares[1]

    # 模擬使用者輸入：
    # 1. 選擇 group (1)
    # 2. 選擇 expense (1)
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    service.delete_expense_ui()

    output = capsys.readouterr().out
    assert "Expense deleted." in output
    assert len(group.expenses) == 0
    
    assert alice.balance == 0
    assert bob.balance == 0