"""
odds.py contains functions for calculating odds and risk / reward
"""

def checkOdds(odds : int) -> None:
    """Check if odds are valid."""
    if odds > -100 and odds < 100:
        raise ValueError("Odds must be less than -100 or greater than 100.")

def checkPct(pct : float) -> None:
    """Check if percentage is valid."""
    if pct < 0 or pct > 1:
        raise ValueError("Percentage must be between 0 and 1.")

def oddsToPct(odds : int) -> float:
    """Convert odds to percentage."""
    checkOdds(odds)
    if odds <= -100:
        return 1 - (100.0 / (100.0 + -odds))
    else:
        return 100.0 / (100.0 + odds)

def pctToOdds(pct : float) -> int:
    """Convert a percentage to odds."""
    checkPct(pct)
    if pct <= 0.5:
        return round((100.0 / pct) - 100)
    else:
        return -round((100.0 / (1 - pct)) - 100)

def oddsToDec(odds : int) -> float:
    """Convert odds to decimal odds."""
    checkOdds(odds)
    if odds <= -100:
        return 1 + (100.0 / -odds)
    else:
        return 1 + (odds / 100.0)

def winnings(odds : int, bet : float = 100.0) -> float:
    """Calculate total winnings from a bet."""
    checkOdds(odds)
    if odds <= -100:
        return bet * (100.0 / (100.0 + -odds))
    else:
        return bet * (odds / 100.0)

def netWinnings(odds : int, bet : float = 100.0) -> float:
    """Calculate net winnings from a bet."""
    checkOdds(odds)
    if odds <= 100:
        return bet * (100.0 / (100.0 + -odds)) - bet
    else:
        return bet * (odds / 100.0) - bet

def expectedValue(winOdds : int, bet : float = 100.0) -> float:
    """Calculate the expected value of a bet."""
    checkOdds(winOdds)
    winPct = oddsToPct(winOdds)
    return round((winPct * winnings(winOdds, bet)) - ((1 - winPct) * bet), 2)

def expectedTrueValue(winOdds : int, trueOdds : int, bet : float = 100.0) -> float:
    """Calculate the expected value of a bet given an underlying true odds."""
    checkOdds(winOdds)
    truePct = oddsToPct(trueOdds)
    return round((truePct * winnings(winOdds, bet)) - ((1 - truePct) * bet), 2)

def minProfitableOdds(trueOdds : int) -> int:
    """Calculate the minimum odds that will be profitable."""
    checkOdds(trueOdds)
    return int(100.0 / (100.0 / trueOdds - 100))

def canArbitrage(odds1 : int, odds2 : int) -> bool:
    """Check if there is an arbitrage opportunity."""
    checkOdds(odds1)
    checkOdds(odds2)
    return (1 / oddsToDec(odds1)) + (1 / oddsToDec(odds2)) < 1

def arbitrageStakes(odds1 : int, odds2 : int, bet : float = 100.0) -> tuple[float, float]:
    """Calculate arbitrage stakes."""
    checkOdds(odds1)
    checkOdds(odds2)

    if canArbitrage(odds1, odds2):
        stake1 = round(bet / (oddsToDec(odds1)), 2)
        stake2 = round(bet / (oddsToDec(odds2)), 2)
        return (stake1, stake2)
    else:
        return (0, 0)

def arbitrageNetWinnings(odds1 : int, odds2 : int, bet : float = 100.0) -> float:
    """Calculate arbitrage net winnings."""
    checkOdds(odds1)
    checkOdds(odds2)

    if canArbitrage(odds1, odds2):
        stakes = arbitrageStakes(odds1, odds2, bet)
        return round(bet - sum(stakes), 2)
    else:
        return 0.00

def arbitragePct(odds1 : int, odds2 : int) -> float:
    """Calculate arbitrage percentage."""
    checkOdds(odds1)
    checkOdds(odds2)

    if canArbitrage(odds1, odds2):
        stakes = arbitrageStakes(odds1, odds2, 100)
        return (100 - sum(stakes)) / 100
    else:
        return 0.00