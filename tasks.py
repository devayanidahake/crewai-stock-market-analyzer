from crewai import Task
from agents import research_agent, analysis_agent, stock_agent, risk_agent, final_agent

# ==========================================================

# TASK 1 : MARKET INTELLIGENCE

# ==========================================================

news_task = Task(
    description="""
You are provided with current market news.

News:
{news}

Perform institutional-grade market analysis.

Your objectives:

1. Identify major market-moving events.

2. Determine whether each event is:

   * Bullish
   * Bearish
   * Neutral

3. Identify sectors likely to benefit.

4. Identify sectors likely to weaken.

5. Explain WHY each sector is affected.

6. Determine expected impact on:

   * NIFTY
   * BANKNIFTY
   * Indian Equities

7. Assign confidence score (0-100).

Avoid generic summaries.

Focus only on information that can influence
capital flows and stock prices.

Return output strictly in JSON format.
""",
    expected_output="""
{
"market_sentiment":"Bullish",
"confidence":85,
"key_events":[
{
"event":"",
"impact":"Bullish",
"reason":""
}
],
"bullish_sectors":[
{
"sector":"",
"reason":""
}
],
"bearish_sectors":[
{
"sector":"",
"reason":""
}
]
}
""",
    agent=research_agent,
)

# ==========================================================

# TASK 2 : TECHNICAL ANALYSIS

# ==========================================================

analysis_task = Task(
    description="""
Analyze the supplied stock dataset.

Stock Data:
{stocks}

Evaluate:

1. RSI strength
2. EMA20 trend
3. EMA50 trend
4. Volume participation
5. Momentum quality
6. Relative sector strength

For each stock:

* Calculate technical conviction.
* Identify trend direction.
* Identify momentum quality.
* Identify breakout probability.

Rank stocks from strongest to weakest.

Only focus on objective data.

Return structured JSON.
""",
    expected_output="""
{
"ranked_stocks":[
{
"symbol":"",
"technical_score":92,
"trend":"Bullish",
"momentum":"Strong",
"breakout_probability":"High"
}
]
}
""",
    agent=analysis_agent,
    context=[news_task],
)

# ==========================================================

# TASK 3 : STOCK SELECTION

# ==========================================================

stock_task = Task(
    description="""
Use:

1. Market Intelligence Report
2. Technical Analysis Report

Determine the best intraday opportunities.

Selection criteria:

* Strong market sentiment
* Strong technical setup
* Sector leadership
* Volume confirmation
* Momentum confirmation

Reject weak candidates.

Select only the TOP 5 stocks.

For each stock provide:

* Symbol
* Recommendation
* Confidence Score
* Technical Reasoning
* Fundamental/News Reasoning
* Risk Level

Rank from strongest to weakest.

Return structured JSON.
""",
    expected_output="""
{
"recommended_stocks":[
{
"rank":1,
"symbol":"",
"recommendation":"BUY",
"confidence":94,
"technical_reason":"",
"news_reason":"",
"risk":"Medium"
}
]
}
""",
    agent=stock_agent,
    context=[news_task, analysis_task],
)

# ==========================================================

# TASK 4 : RISK MANAGEMENT

# ==========================================================

risk_task = Task(
    description="""
Create executable trading plans for
all recommended stocks.

For every stock determine:

1. Entry Price
2. Stop Loss
3. Target 1
4. Target 2
5. Risk Reward Ratio
6. Trade Quality Score
7. Position Risk Assessment

Reject trades where:

Risk Reward < 1:2

Clearly explain:

* Why stop loss was selected
* Why target was selected

Output must be practical and ready
for execution.

Return structured JSON.
""",
    expected_output="""
{
"trade_plans":[
{
"symbol":"",
"entry_price":0,
"stop_loss":0,
"target_1":0,
"target_2":0,
"risk_reward":"1:2.5",
"trade_quality_score":92,
"risk_level":"Low"
}
]
}
""",
    agent=risk_agent,
    context=[stock_task],
)

# ==========================================================

# TASK 4 : FINAL REPORT TASK

# ==========================================================
final_report_task = Task(
        description="""
    Create the final trading report.

    Combine:

    - Market Intelligence
    - Technical Analysis
    - Stock Selection
    - Risk Assessment

    Return a final actionable report.
    """,
        expected_output="""
    {
    "market_view":"",
    "best_stock":"",
    "top_5":[],
    "risk_summary":""
    }
    """,
        agent=final_agent,
        context=[
            news_task,
            analysis_task,
            stock_task,
            risk_task
        ],
)