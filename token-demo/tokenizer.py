import os

# 1. 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. 拼接出我们刚才创建的缓存文件夹的绝对路径
cache_dir = os.path.join(current_dir, "tiktoken_cache")

# 3. 【关键】在导入 tiktoken 之前，设置环境变量
os.environ["TIKTOKEN_CACHE_DIR"] = cache_dir

# 4. 现在再导入 tiktoken
import tiktoken

def count_tokens(text, model="gpt-4"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)
    return len(tokens), tokens

# --- 测试示例 ---
if __name__ == "__main__":
    while True:
        sample_text = input("请输入要计算的文本（输入后直接按一次回车结束，输入 'q' 退出）：")

        if sample_text.lower() == 'q':
            break

        if sample_text.strip():  # 防止不小心只按了回车导致空输入报错
            token_count, token_list = count_tokens(sample_text)
            print(f"Token 总数: {token_count}")
            print(f"Token 拆分详情: {token_list}")
            print("-" * 40)

def something_else():
    input_str = input("请输入要计算的文本：")
    print(input_str)