import pytest

from utils.calculation import split_amount
from utils import storage
from models.user import User
from models.group import Group

# ---------------------------
# split_amount 測試
# ---------------------------
def test_split_amount_even():
    participants = ["Alice", "Bob", "Charlie", "David"]
    amounts = split_amount(100, participants)
    assert amounts == [25, 25, 25, 25]

def test_split_amount_uneven():
    participants = ["Alice", "Bob", "Charlie"]
    amounts = split_amount(10, participants)
    # 因為你的 function 平均分，可能是浮點數
    assert sum(amounts) == pytest.approx(10)

# ---------------------------
# storage.py 測試
# ---------------------------
def test_load_save_data(tmp_path):
    """使用臨時檔案測試 load_data & save_data"""
    DATA_FILE = tmp_path / "data.json"

    # 建立 sample data
    users = {"Alice": User("Alice"), "Bob": User("Bob")}
    groups = [Group("Trip")]
    data = {"users": users, "groups": groups}

    # 暫時覆蓋 storage.DATA_FILE
    storage.DATA_FILE = str(DATA_FILE)

    # 儲存
    storage.save_data(data)
    # 讀取
    loaded = storage.load_data()

    # 驗證 user 名稱
    assert set(loaded["users"].keys()) == set(users.keys())
    # 驗證 group 名稱
    assert loaded["groups"][0].name == "Trip"
