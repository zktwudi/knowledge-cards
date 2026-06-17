# cards.py - 个人知识卡片管理器 (第1版：只有菜单骨架)
import json
import os

DATA_FILE = "cards_data.json"

def load_cards():
    """从文件加载卡片，如果文件不存在或为空，返回空列表"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_cards(cards):
    """把卡片列表保存到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def main():
    cards = load_cards()  # 所有卡片都放在这里，每一张都是一个 dict
    print("📇 欢迎使用知识卡片管理器！")

    while True:
        # 打印菜单
        print("\n" + "=" * 30)
        print("[1] 添加卡片")
        print("[2] 查看所有卡片")
        print("[3] 搜索卡片")
        print("[4] 删除卡片")
        print("[0] 退出")
        print("=" * 30)

        choice = input("请选择操作 (0-4): ").strip()

        if choice == "0":
            save_cards(cards)
            print("👋 再见！")
            break
        elif choice == "1":
            title = input("请输入卡片标题: ").strip()
            content = input("请输入卡片内容: ").strip()
            if not title or not content:
                print("⚠️ 标题和内容不能为空！")
                continue  # 跳过本次循环，回到菜单

            # 生成一个简单的 ID：用当前卡片的数量 + 1
            new_id = len(cards) + 1
            card = {"id": new_id, "title": title, "content": content}
            cards.append(card)
            print(f"✅ 卡片 #{new_id} 已添加！")
        elif choice == "2":
            if not cards:
                print("📭 目前没有任何卡片。")
            else:
                print("\n--- 所有知识卡片 ---")
                for card in cards:
                    print(f"[{card['id']}] {card['title']}")
                    print(f"    {card['content']}\n")
        elif choice == "3":
            keyword = input("请输入搜索关键词: ").strip().lower()
            if not keyword:
                print("⚠️ 关键词不能为空！")
                continue

            matched = []
            for card in cards:
                # 把标题和内容都转成小写，这样搜索不区分大小写
                title_lower = card["title"].lower()
                content_lower = card["content"].lower()
                if keyword in title_lower or keyword in content_lower:
                    matched.append(card)

            if not matched:
                print(f"🔍 没有找到包含 '{keyword}' 的卡片。")
            else:
                print(f"--- 搜索 '{keyword}' 的结果 ({len(matched)} 条) ---")
                for card in matched:
                    print(f"[{card['id']}] {card['title']}")
                    print(f"    {card['content']}\n")
        elif choice == "4":
            if not cards:
                print("📭 没有卡片可删。")
                continue

            try:
                card_id = int(input("请输入要删除的卡片 ID: ").strip())
            except ValueError:
                print("⚠️ ID 必须是一个数字！")
                continue

                # 查找要删除的卡片
            card_to_delete = None
            for card in cards:
                if card["id"] == card_id:
                    card_to_delete = card
                    break

            if card_to_delete is None:
                print(f"❌ 未找到 ID 为 {card_id} 的卡片。")
            else:
                cards.remove(card_to_delete)
                print(f"🗑️  卡片 #{card_id} '{card_to_delete['title']}' 已删除。")
        else:
            print("⚠️ 输入错误，请输入数字 0-4")

# 这一行是 Python 的约定：当直接运行这个文件时，才执行 main()
if __name__ == "__main__":
    main()