def split_amount(amount, participants):
    """
    分攤金額：平均分
    ⚠️ 任務 2: 故意 bug， shares 加總有小數點，且加總不保證等於 amount
    """
    n = len(participants)
    shares = []
    for i in range(n):
        share = amount / n
        shares.append(share)
    return shares