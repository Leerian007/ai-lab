import json

# ==========================================
# 1. 模拟数据准备
# ==========================================
# 假设这是你和 AI 的完整对话（父文档）
full_conversation = (
    "用户：我最近在用 Java 写车联网平台。"
    "AI：Java 在企业级开发中很稳定，有什么具体需求吗？"
    "用户：我想在平台里加入区块链的合约交易功能。"
    "AI：这是一个很好的跨界结合！你可以考虑学习 Solidity。"
    "用户：那 Solidity 和 Rust 哪个更适合智能合约开发？"
)

# 模拟切块后的数据（子文档）
# 在实际工程中，这些会被转化为向量（Vector）存入数据库
chunks = [
    {"id": "chunk_1", "parent_id": "doc_01", "text": "用户：我最近在用 Java 写车联网平台。"},
    {"id": "chunk_2", "parent_id": "doc_01", "text": "AI：Java 在企业级开发中很稳定，有什么具体需求吗？"},
    {"id": "chunk_3", "parent_id": "doc_01", "text": "用户：我想在平台里加入区块链的合约交易功能。"},
    {"id": "chunk_4", "parent_id": "doc_01", "text": "AI：这是一个很好的跨界结合！你可以考虑学习 Solidity。"},
    {"id": "chunk_5", "parent_id": "doc_01", "text": "用户：那 Solidity 和 Rust 哪个更适合智能合约开发？"},
]

# ==========================================
# 2. 核心逻辑：模拟检索与组装
# ==========================================
def rag_parent_retrieval(user_query, chunks, full_text):
    print(f"👤 用户当前提问: {user_query}")
    print("-" * 40)

    # 【第一步：小块检索】
    # 在实际中，这里会调用向量数据库 (如 FAISS) 进行相似度计算
    # 这里我们用简单的字符串包含来模拟“命中了第4块”
    matched_chunk = None
    for chunk in chunks:
        if "Solidity" in chunk["text"] and "跨界" in chunk["text"]:
            matched_chunk = chunk
            break

    if matched_chunk:
        print(f"🔍 [小块检索] 命中了子块: {matched_chunk['text']}")

        # 【第二步：大块返回】
        # 根据子块的 parent_id，直接去原始完整对话中把整段内容拿出来
        # （这里简化为直接返回完整对话，实际中可能是返回包含该子块的完整段落）
        retrieved_context = full_text

        print(f"📦 [大块返回] 提取给大模型的完整上下文:\n{retrieved_context}")
        print("-" * 40)

        # 【第三步：组装 Prompt】
        final_prompt = f"参考以下历史对话：\n{retrieved_context}\n\n回答用户最新问题：{user_query}"
        return final_prompt

# ==========================================
# 3. 运行测试
# ==========================================
if __name__ == "__main__":
    query = "我刚才问的编程语言是什么来着？"
    prompt = rag_parent_retrieval(query, chunks, full_conversation)

    print("🚀 [最终发送给大模型的 Prompt]:")
    print(prompt)