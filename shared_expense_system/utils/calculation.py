def split_amount(amount, participants):
    """
    分攤金額：平均分
    💡 任務 1: 可重構
    ⚠️ 任務 2: 故意 bug: payer 在 participants 會多扣一次
    """
    n = len(participants)
    shares = []
    for i in range(n):
        share = amount / n
        shares.append(share)
    return shares
