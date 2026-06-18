from crewai import Crew, Process

from agents import research_agent, analysis_agent, stock_agent, risk_agent, final_agent

from tasks import news_task, analysis_task, stock_task, risk_task, final_report_task

crew = Crew(
    agents=[research_agent, analysis_agent, stock_agent, risk_agent, final_agent],
    tasks=[news_task, analysis_task, stock_task, risk_task, final_report_task],
    process=Process.sequential,
    verbose=True,
)
