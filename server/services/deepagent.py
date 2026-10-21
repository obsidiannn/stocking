# 文件路径：hello_agent.py

import os
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI

# 使用 ChatOpenAI 并将 base_url 指向 DeepSeek，这是最直接的接入方式
model = ChatOpenAI(
    model="deepseek-v4.1-flash",          
    api_key=os.environ["OPENAI_API_KEY"],  
    base_url=os.environ["OPENAI_BASE_URL"],   
)

# 定义一个简单的自定义工具，函数的 docstring 就是工具描述
def get_weather(city: str) -> str:
    """查询指定城市的天气。"""
    # 实际项目中这里会调用真实天气 API
    return f"{city} 今天晴天，气温 25°C，适合出行。"

# 创建 Agent，传入模型实例和工具列表
agent = create_deep_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个友好的助手，能够查询天气信息。",
)

# 调用 Agent，messages 接受 OpenAI 风格的消息格式
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京今天天气怎么样？"}]
})

# 打印 Agent 的最终回复
print(result["messages"][-1].content)