import os
from openai import OpenAI

# ========== 配置区域 ==========
# 方式一：直接填写 API Key（不推荐，容易泄露）
# API_KEY = "sk-你的API密钥"

# 方式二：从环境变量读取（推荐）
# API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_KEY = "sk-3e5e760d28884fd59093bf0bfeb86101"
if not API_KEY:
    print("错误：请设置环境变量 DEEPSEEK_API_KEY")
    print("或在代码中直接填写 API_KEY 变量")
    exit(1)

# 初始化客户端
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"  # DeepSeek API 地址[reference:0][reference:1]
)

# 模型选择（推荐使用 deepseek-v4-pro）[reference:2]
MODEL = "deepseek-v4-pro"


def chat_with_deepseek(user_message, history=None):
    """
    调用 DeepSeek API 进行对话

    Args:
        user_message: 用户输入的消息
        history: 历史对话列表，用于多轮对话

    Returns:
        response: API 返回的完整响应对象
        updated_history: 更新后的历史记录
    """
    if history is None:
        history = []

    # 添加用户消息到历史
    history.append({"role": "user", "content": user_message})

    try:
        # 调用 API[reference:3]
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            stream=False,
            # 可选：启用思考模式（DeepSeek V4 支持）
            # reasoning_effort="high",
            # extra_body={"thinking": {"type": "enabled"}}
        )

        # 获取助手回复
        assistant_reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_reply})

        return response, history

    except Exception as e:
        print(f"API 调用出错：{e}")
        return None, history


def main():
    """主程序：终端交互循环"""
    print("=" * 50)
    print("DeepSeek 终端对话程序")
    print(f"当前模型：{MODEL}")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'clear' 清空对话历史")
    print("=" * 50)

    history = []  # 保存对话历史，支持多轮对话[reference:4]

    while True:
        try:
            # 获取用户输入
            user_input = input("\n你：").strip()

            # 退出命令
            if user_input.lower() in ["quit", "exit"]:
                print("再见！")
                break

            # 清空历史
            if user_input.lower() == "clear":
                history = []
                print("对话历史已清空")
                continue

            # 空输入跳过
            if not user_input:
                continue

            # 调用 API
            print("DeepSeek 正在思考...", end="", flush=True)
            response, history = chat_with_deepseek(user_input, history)
            print("\r" + " " * 20 + "\r", end="")  # 清除"正在思考"提示

            if response:
                print(f"DeepSeek：{response.choices[0].message.content}")
            else:
                print("请求失败，请重试")

        except KeyboardInterrupt:
            print("\n\n程序已中断")
            break
        except Exception as e:
            print(f"发生错误：{e}")


if __name__ == "__main__":
    main()