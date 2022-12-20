"""
odds.py contains functions for calculating odds and risk / reward
"""

def oddsToPct(odds):
    # Convert odds to a percentage
    if odds < 0:
        return 1 - (100.0 / (100.0 + -odds))
    else:
        return 100.0 / (100.0 + odds)

def pctToOdds(pct):
    # Convert a percentage to odds
    if pct < 0.5:
        return round((100.0 / pct) - 100)
    else:
        return -round((100.0 / (1 - pct)) - 100)

def oddsToDec(odds):
    # Convert odds to decimal odds
    if odds < 0:
        return 1 + (100.0 / -odds)
    else:
        return 1 + (odds / 100.0)

def winnings(odds, bet=100.0):
    # Calculate winnings from a bet
    if odds < 0:
        return bet * (100.0 / (100.0 + -odds))
    else:
        return bet * (odds / 100.0)

def netWinnings(odds, bet=100.0):
    # Calculate net winnings from a bet
    if odds < 0:
        return bet * (100.0 / (100.0 + -odds)) - bet
    else:
        return bet * (odds / 100.0) - bet

def expectedValue(winOdds, bet=100.0):
    # Calculate the expected value of a bet
    winPct = oddsToPct(winOdds)
    return round((winPct * winnings(winOdds, bet)) - ((1 - winPct) * bet), 2)

def expectedTrueValue(winOdds, trueOdds, bet=100.0):
    # Calculate the expected value of a bet with a true odds
    truePct = oddsToPct(trueOdds)
    return round((truePct * winnings(winOdds, bet)) - ((1 - truePct) * bet), 2)

def canArbitrage(odds1, odds2):
    # Determine if there is an arbitrage opportunity
    return (1 / oddsToDec(odds1)) + (1 / oddsToDec(odds2)) < 1

def arbitrageStakes(odds1, odds2, bet=100.0):
    # Calculate the arbitrage stakes
    if canArbitrage(odds1, odds2):
        stake1 = round(bet / (oddsToDec(odds1)), 2)
        stake2 = round(bet / (oddsToDec(odds2)), 2)
        return (stake1, stake2)
    else:
        return (0, 0)

def arbitrageNetWinnings(odds1, odds2, bet=100.0):
    # Calculate the arbitrage winnings
    if canArbitrage(odds1, odds2):
        stakes = arbitrageStakes(odds1, odds2, bet)
        return round(bet - sum(stakes), 2)
    else:
        return 0

def arbitragePct(odds1, odds2):
    # Calculate the arbitrage percentage
    if canArbitrage(odds1, odds2):
        stakes = arbitrageStakes(odds1, odds2, 100)
        return (100 - sum(stakes)) / 100
    else:
        return 0