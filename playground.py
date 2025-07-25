import openai
from phi.agent import Agent
import phi.api
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os
import phi
from phi.playground import Playground, serve_playground_app

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

phi.app = os.getenv("PHI_API_KEY")

web_serch_agent = Agent(
    name="Web Search Agent",
    role="web_search_agent_for_retrieving_information",
    model=OpenAIChat(model="gpt-4o"),
    tools=[DuckDuckGo()],
    instructions=[
        "always include the source of the information you find in your response"
    ],
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="finance_agent_for_retrieving_financial_information",
    model=OpenAIChat(model="gpt-4o"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
            key_financial_ratios=True,
        )
    ],
    instructions=["use tables to present financial data clearly"],
    show_tool_calls=True,
    markdown=True,
)

app = Playground(agents=[web_serch_agent, finance_agent]).get_app()
if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True, port=8000)
