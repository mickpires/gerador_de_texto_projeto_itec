from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from itec import OPENROUTER_API_KEY

llm = ChatOpenAI(
    model = 'openrouter/deepseek/deepseek-chat-v3.1:free',
    base_url = 'https://openrouter.ai/api/v1',
    openai_api_key = OPENROUTER_API_KEY
)