from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app
from dotenv import load_dotenv

load_dotenv()

web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for current information and news",
    model=Ollama(model="llama3.1:8b"),
    tools=[DuckDuckGo()],
    instructions=[
        "ALWAYS search for information using the DuckDuckGo tool before responding",
        "Include sources and links in your responses",
        "Provide accurate and up-to-date information",
        "Be comprehensive but organized in your explanations",
        "If search fails, acknowledge it and provide what you know",
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Provide financial data, analysis, and investment insights",
    model=Ollama(model="llama3.1:8b"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
            key_financial_ratios=True,
        )
    ],
    instructions=[
        "ALWAYS use YFinance tools to get current financial data",
        "Present financial data in clear, organized tables",
        "Provide context and analysis with the data",
        "Include relevant financial metrics and ratios",
        "Explain complex financial terms in simple language",
        "Mention that this is for informational purposes only, not financial advice",
        "If data retrieval fails, explain what went wrong",
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

multi_AI_agent = Agent(
    model=Ollama(model="llama3.1:8b"),
    team=[web_search_agent, finance_agent],
    instructions=[
        "Collaborate with team members to provide comprehensive answers",
        "Utilize each agent's strengths and expertise",
        "Ensure all information is accurate and well-sourced",
        "Maintain a user-friendly and informative response style",
    ],
    show_tool_calls=True,
    markdown=True,
)

multi_AI_agent.print_response("What are the latest trends in technology and finance?")
# app = Playground(agents=[web_search_agent, finance_agent]).get_app()

# if __name__ == "__main__":
#     serve_playground_app("playground:app", reload=False, port=8000)
