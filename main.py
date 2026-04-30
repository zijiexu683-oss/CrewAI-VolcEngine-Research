import os
from crewai import Agent, Task, Crew, Process

# ===================== 1. 豆包 API 配置 =====================
# 填入你刚刚找到的单行 API Key
os.environ["VOLCENGINE_API_KEY"] = os.getenv("VOLCENGINE_API_KEY", "在此处填入你的API_KEY")
# 填入你刚才截图中那个绿色的模型 ID (注意保留 volcengine/ 前缀)
MODEL_STRING = "volcengine/doubao-seed-2-0-pro-260215" 

# ===================== 2. Agent 定义 =====================
# 下面的代码一个字都不用改，直接照旧！
researcher = Agent(
    role='资深市场调研员',
    goal='深入分析 {topic} 领域的最新技术趋势',
    backstory="你擅长从海量信息中提取核心数据，能够识别出新兴技术和潜在的市场机会。",
    verbose=True,
    allow_delegation=False,
    llm=MODEL_STRING
)

# ... 后面的 validator, writer, task 和 crew 保持原样 ...

validator = Agent(
    role='信息质检专家',
    goal='对调研报告中的事实进行验证',
    backstory="你对数据极其敏感，负责指出调研结果中逻辑不通或缺乏证据支持的部分。",
    verbose=True,
    llm=MODEL_STRING
)

writer = Agent(
    role='专业技术撰稿人',
    goal='撰写一份结构化且易于阅读的研报',
    backstory="你擅长将复杂的调研数据转化为深入浅出的专业文档。",
    verbose=True,
    llm=MODEL_STRING
)

# ===================== 3. Task 定义 (已补全 expected_output) =====================
task1 = Task(
    description='搜索关于 {topic} 的 5 个最新突破点。', 
    expected_output='一段包含 5 个最新技术突破点的简要列表。',
    agent=researcher
)

task2 = Task(
    description='核实这些突破点的技术真实性，剔除虚假宣传。', 
    expected_output='一份经过事实核查的突破点清单，标明哪些是真实的，哪些是缺乏依据的。',
    agent=validator
)

task3 = Task(
    description='根据验证后的信息编写一份 800 字的研报。', 
    expected_output='一份排版整洁、逻辑清晰、不少于 800 字的专业研究报告，使用 Markdown 格式。',
    agent=writer
)

# ===================== 4. Crew 运行 =====================
crew = Crew(
    agents=[researcher, validator, writer],
    tasks=[task1, task2, task3],
    process=Process.sequential
)

# 开始执行
print("🚀 正在启动多智能体协作流程，请稍候...")
result = crew.kickoff(inputs={'topic': '大语言模型中的多智能体协作技术'})

print("\n" + "="*50)
print("✅ 最终研报结果：")
print("="*50)
print(result)