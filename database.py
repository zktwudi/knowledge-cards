import sqlite3

DB_FILE = 'cards.db'

def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 让返回的行可以像字典一样访问
    return conn

def init_db():
    """初始化数据库：建表（如果不存在）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_cards():
    """返回所有卡片，每张卡片是一个字典"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content FROM cards ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    # 把 Row 对象转成字典列表
    return [dict(row) for row in rows]

def add_card(title, content):
    """添加卡片，返回新卡片的 id"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cards (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def search_cards(keyword):
    """搜索标题或内容包含关键词的卡片，返回字典列表"""
    conn = get_connection()
    cursor = conn.cursor()
    # 用 LIKE 做模糊匹配，% 表示任意字符
    query = 'SELECT id, title, content FROM cards WHERE title LIKE ? OR content LIKE ? ORDER BY id'
    param = f'%{keyword}%'
    cursor.execute(query, (param, param))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_card_by_id(card_id):
    """根据 id 获取单张卡片，如果没有返回 None"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content FROM cards WHERE id = ?', (card_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_card(card_id, title, content):
    """更新卡片，返回是否成功（影响行数 > 0）"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE cards SET title = ?, content = ? WHERE id = ?', (title, content, card_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def delete_card(card_id):
    """删除卡片，返回是否成功"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0