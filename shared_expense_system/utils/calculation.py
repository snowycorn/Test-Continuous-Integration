def split_amount(amount, participants):
    '''
    shares round to integer
    adjust the rounding difference by the last participant's share
    '''
    n = len(participants)
    base_share = round(amount / n)
    shares = [base_share for _ in range(n)]
    diff = int(amount - sum(shares))
    if diff != 0:
        shares[-1] += diff
    return shares