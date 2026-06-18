def calculate_score(stock):
    score = 0
    reasons = []

    if stock["price"] > stock["ema20"]:
        score += 20
        reasons.append("Price above EMA20")

    if stock["ema20"] > stock["ema50"]:
        score += 20
        reasons.append("EMA20 above EMA50")

    rsi = stock["rsi"]

    if 55 <= rsi <= 70:
        score += 30
        reasons.append(f"Healthy RSI ({rsi:.1f})")

    if stock.get("macd", 0) > stock.get("macd_signal", 0):
        score += 20
        reasons.append("Bullish MACD crossover")

    if stock["volume"] > 1_000_000:
        score += 10
        reasons.append("Strong volume")

    return score, reasons


def rank_stocks(stocks):

    for stock in stocks:
        score, reasons = calculate_score(stock)

        stock["score"] = score
        stock["reasons"] = reasons

    return sorted(stocks, key=lambda x: x["score"], reverse=True)
