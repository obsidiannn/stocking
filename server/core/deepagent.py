# 文件路径：hello_agent.py

import os
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from server.services import kline_service

# 使用 ChatOpenAI 并将 base_url 指向 DeepSeek，这是最直接的接入方式
model = ChatOpenAI(
    model="deepseek-flash",          
    api_key=os.environ["OPENAI_API_KEY"],  
    base_url=os.environ["OPENAI_BASE_URL"],   
)


def get_index_membership():
    pass

def query_kline_day(market: str, code: str):
    pass

def query_kline_week():
    pass

def query_index_day():
    pass

def query_index_week():
    pass


agent = create_deep_agent(
    model=model,
    tools=[query_kline_day, query_kline_week, query_index_day, query_index_week,get_index_membership ],
    # backend="./resource/agent/",
    # memory="./resource/memory/",
    system_prompt="",
)
