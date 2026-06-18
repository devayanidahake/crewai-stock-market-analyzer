from crew import crew

from tools.news_tool import get_market_news
from tools.stock_tool import get_stock_data
from tools.scoring_tool import rank_stocks

from datetime import datetime
import os


def main():
    try:
        print("\n==============================")
        print("Fetching Market News...")
        print("==============================")

        news = get_market_news()

        print(f"News Articles Found: {len(news)}")

        print("\n==============================")
        print("Fetching Stock Data...")
        print("==============================")

        stocks = get_stock_data()

        print(f"Stocks Analyzed: {len(stocks)}")

        print("\n==============================")
        print("Ranking Stocks...")
        print("==============================")

        ranked_stocks = rank_stocks(stocks)

        print("\nTop Ranked Stocks:")

        for stock in ranked_stocks[:5]:
            print(f"{stock['symbol']} | Score={stock['score']}")

        print("\n==============================")
        print("Running CrewAI Analysis...")
        print("==============================")

        top_stocks = ranked_stocks[:10]

        today = datetime.now().strftime("%d-%m-%Y")

        for stock in top_stocks:
            stock.pop("reasons", None)

        result = crew.kickoff(
            inputs={"date": today, "news": news, "stocks": top_stocks}
        )

        print("\n==============================")
        print("FINAL REPORT")
        print("==============================")

        print(result)

        os.makedirs("reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_path = f"reports/report_{timestamp}.md"

        with open(report_path, "w", encoding="utf-8") as file:
            file.write(str(result))

        print(f"\nReport Saved: {report_path}")

    except Exception as e:
        print(f"\nApplication Error: {str(e)}")

if __name__ == "__main__":
    print("MAIN IS RUNNING")
    main()
