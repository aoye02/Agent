class MemoryManager:
    """分层记忆：滑动窗口 + 摘要"""

    def __init__(self, db, summarizer_model):
        self.db = db
        self.summarizer_model = summarizer_model   # 传入一个模型对象用来生成摘要

    def build_context(self, conv_id, current_question):
        """组装发给模型的消息列表（无死角滑动窗口）"""
        # 1. 读该对话的所有消息
        all_msgs = self.db.get_messages(conv_id, limit=None) # 确保拿全量
        total_msgs = len(all_msgs)

        # 2. 获取已有摘要（字符串）
        summary = self.db.get_summary(conv_id)

        # 3. 假设已有摘要代表了前面的 N 条消息（简化处理：我们通过总数来反推）
        # 为了保证逻辑简单且不丢消息，我们用一种更直接的方法：
        # 每次超出 10 条，我们就更新摘要，并把之前发给模型的历史截断。

        # ★ 核心策略：每次凑够 10 条新消息，更新一次摘要。
        # 我们需要记录“上次摘要时的消息总数”（可以存在内存里，或者查数据库，这里用内存字典模拟）
        if not hasattr(self, "_summary_point"):
            self._summary_point = {}  # 记录每个 conv_id 上次摘要到了第几条

        last_point = self._summary_point.get(conv_id, 0)
        unsummarized_count = total_msgs - last_point

        # 如果未被摘要的消息达到了 10 条，触发摘要更新
        if unsummarized_count >= 30:
            # 把这 10 条（或更多）生成新摘要
            new_msgs_to_summarize = all_msgs[last_point:total_msgs]
            summary = self._summarize(new_msgs_to_summarize, old_summary=summary)
            self.db.save_summary(conv_id, summary)
            # 更新游标
            self._summary_point[conv_id] = total_msgs

        # 4. 组装上下文
        messages = []

        system_content = (
            "【极其重要的系统设定】\n"
            "你是一个拥有长期记忆的专属 AI 助理。你已经和用户进行了多次对话，你们有共同的历史记忆。\n"
            "绝对不允许再说出“作为AI我没有记忆”、“每次对话都是新开始”、“我无法访问历史记录”这类话。\n"
            "如果你看到下方的历史摘要或近期聊天记录中包含了用户的信息（如名字、偏好），你必须牢牢记住并基于此回答。"
        )

        # 注入摘要
        if summary:
            system_content += f"\n\n【过往历史记忆摘要】\n{summary}"
        messages.append({"role": "system", "content": system_content})
        # ★ 关键：把“还没被摘要的”消息，全部发给模型
        # 注意：如果 35 条时，摘要吞了前 30 条，这里就把 31~35 条全发过去。
        # 如果超过 20 条，为了防止太长，我们可以只发最后 20 条未摘要的（但因为有 10 条就摘要的机制，未摘要的永远不会超过 10 条，所以全发即可！）

        # 重新获取一下游标，因为上面可能刚更新过
        current_point = self._summary_point.get(conv_id, 0)
        messages_to_send = all_msgs[current_point:]

        for msg_id, role, content in messages_to_send:
                messages.append({"role": role, "content": content})

        # 如果历史消息里的最后一条，就是当前的 question，说明数据库刚存进去，不用再重复加
        if not (messages and messages[-1]["role"] == "user" and messages[-1]["content"] == current_question):
            messages.append({"role": "user", "content": current_question})

        # print("\n======== 帮厨端出来的菜（发给模型的消息） ========")
        # for m in messages:
        #     print(f"[{m['role']}]: {m['content'].encode('gbk', errors='ignore').decode('gbk')}...")
        # print("==================================================\n")

        return messages

    def _summarize(self, messages, old_summary=""):
        """调用便宜的模型生成摘要"""
        # 拼接历史文本
        text = "\n".join(f"{m[1]}: {m[2]}" for m in messages)
        prompt = f"""你是一个专业的对话记录员。
        以下是对话的早期摘要（可能为空）：
        {old_summary}

        现在有了最新的几条对话记录：
        {text}

        请将上述内容合并，用 200 字左右总结整个对话的关键信息。
        保留：用户提到的事实、偏好、重要决定。
        忽略：寒暄、重复的废话。

        摘要："""
        try:
            result = self.summarizer_model.invoke(prompt)
            return result.content
        except Exception as e:
            print(f"生成摘要失败: {e}")
            # 失败了就返回旧摘要，保证记忆不倒退
            return old_summary if old_summary else "（历史摘要生成失败）"