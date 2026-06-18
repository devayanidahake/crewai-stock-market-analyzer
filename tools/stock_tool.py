import yfinance as yf
import ta

WATCHLIST = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "HDFCBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "TATAMOTORS.NS",
]

def get_trend(price, ema20, ema50):

    if price > ema20 > ema50:
        return "STRONG_BULLISH"

    elif price > ema20:
        return "BULLISH"

    elif price < ema20 < ema50:
        return "STRONG_BEARISH"

    return "NEUTRAL"


def get_recommendation(score):

    if score >= 80:
        return "STRONG_BUY"

    elif score >= 60:
        return "BUY"

    elif score >= 40:
        return "WATCH"

    return "AVOID"


def get_conviction(score):

    if score >= 80:
        return "HIGH"

    elif score >= 60:
        return "MEDIUM"

    return "LOW"


def get_trade_levels(stock):

    price = stock["price"]
    atr = stock["atr"]

    return {
        "entry": round(price, 2),
        "stop_loss": round(price - atr, 2),
        "target_1": round(price + (atr * 2), 2),
        "target_2": round(price + (atr * 3), 2),
    }

def calculate_score(stock):
    score = 0
    reasons = []

    # Trend
    if stock["price"] > stock["ema20"]:
        score += 20
        reasons.append("Price above EMA20")

    if stock["ema20"] > stock["ema50"]:
        score += 20
        reasons.append("EMA20 above EMA50")

    # RSI
   
    rsi = stock["rsi"]

    if 55 <= rsi <= 65:
        score += 25
        reasons.append(f"Healthy RSI ({rsi})")

    elif 65 < rsi <= 75:
        score += 15
        reasons.append(f"Strong RSI ({rsi})")

    elif 50 <= rsi < 55:
        score += 10

    elif rsi > 75:
        score -= 10
        reasons.append("Overbought RSI")

    # MACD
    if stock["macd"] > stock["macd_signal"]:
        score += 25
        reasons.append("Bullish MACD")

    # Relative Volume
    if stock["relative_volume"] > 1.5:
        score += 10
        reasons.append(
            f"High Relative Volume ({stock['relative_volume']})"
        )

    return score, reasons


def rank_stocks(stocks):

    for stock in stocks:

        score, reasons = calculate_score(stock)

        stock["score"] = score
        stock["reasons"] = reasons

        stock["recommendation"] = (
            get_recommendation(score)
        )

        stock["conviction"] = (
            get_conviction(score)
        )

        trade_levels = get_trade_levels(stock)

        stock.update(trade_levels)

    return sorted(
        stocks,
        key=lambda x: x["score"],
        reverse=True
    )

def get_stock_data():

    stocks = []

    for symbol in WATCHLIST:

        try:

            ticker = yf.Ticker(symbol)

            hist = ticker.history(period="6mo")

            if hist.empty:
                continue

            close = hist["Close"]

            current_price = float(close.iloc[-1])

            # RSI
            rsi = ta.momentum.RSIIndicator(close).rsi().iloc[-1]

            # EMA
            ema20 = ta.trend.EMAIndicator(
                close,
                window=20
            ).ema_indicator().iloc[-1]

            ema50 = ta.trend.EMAIndicator(
                close,
                window=50
            ).ema_indicator().iloc[-1]

            # MACD
            macd_indicator = ta.trend.MACD(close)

            macd = macd_indicator.macd().iloc[-1]
            macd_signal = (
                macd_indicator.macd_signal().iloc[-1]
            )

            # ATR
            atr = ta.volatility.AverageTrueRange(
                hist["High"],
                hist["Low"],
                hist["Close"]
            ).average_true_range().iloc[-1]

            # Volume
            volume = int(hist["Volume"].iloc[-1])

            avg_volume = (
                hist["Volume"]
                .tail(20)
                .mean()
            )

            relative_volume = (
                volume / avg_volume
                if avg_volume > 0
                else 0
            )
            
            trend = get_trend(
            current_price,
            ema20,
            ema50
            )

            stocks.append(
            {
                "symbol": symbol,
                "price": round(current_price, 2),

                "volume": volume,
                "relative_volume": round(relative_volume, 2),

                "rsi": round(rsi, 2),

                "ema20": round(ema20, 2),
                "ema50": round(ema50, 2),

                "macd": round(macd, 2),
                "macd_signal": round(macd_signal, 2),

                "atr": round(atr, 2),
                "trend": trend
            }
        )

        except Exception as e:
            print(f"Error processing {symbol}: {e}")

    return stocks


if __name__ == "__main__":

    stocks = get_stock_data()

    ranked = rank_stocks(stocks)

    print("\nTOP STOCKS\n")

    for stock in ranked[:5]:

        print(
            f"""
            Symbol: {stock['symbol']}

            Score: {stock['score']}
            Recommendation: {stock['recommendation']}
            Conviction: {stock['conviction']}

            Trend: {stock['trend']}
            Price: {stock['price']}
            RSI: {stock['rsi']}
            ATR: {stock['atr']}

            Entry: {stock['entry']}
            Stop Loss: {stock['stop_loss']}
            Target 1: {stock['target_1']}
            Target 2: {stock['target_2']}

            Relative Volume: {stock['relative_volume']}

            Reasons:
            {", ".join(stock['reasons'])}
            """
            )