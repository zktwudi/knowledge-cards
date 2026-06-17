from flask import Flask, request, redirect, url_for, render_template
import database  # 我们刚写的数据访问层
import json
import os

app = Flask(__name__)
# 初始化数据库
database.init_db()

@app.route('/')
def index():
    cards = database.get_all_cards()
    return render_template('index.html', cards=cards)

# 显示添加表单
@app.route('/add')
def add_form():
    return '''
    <h1>添加新卡片</h1>
    <form method="post" action="/add">
        <p>标题: <input type="text" name="title" required></p>
        <p>内容: <br><textarea name="content" rows="4" required></textarea></p>
        <button type="submit">✅ 添加</button>
    </form>
    <a href="/">← 返回首页</a>
    '''

# 处理添加请求
@app.route('/add', methods=['POST'])
def add_card():
    title = request.form['title'].strip()
    content = request.form['content'].strip()
    if not title or not content:
        return "标题和内容不能为空！<a href='/add'>返回</a>"

    database.add_card(title, content)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    keyword = request.args.get('q', '').strip().lower()
    if not keyword:
        return redirect(url_for('index'))
    # 数据库的搜索函数已经处理了大小写（SQLite LIKE 不区分英文大小写）
    # 但为了保证中文也能统一，我们可以在函数里做处理（当前已OK）
    results = database.search_cards(keyword)
    # 搜索结果我们之前用内联 HTML，这里继续用模板更好，但为了不引入新模板，
    # 可以沿用原来的内联 HTML 生成方式，或者用模板。
    # 这里我们使用一个简单的内联 HTML，像之前一样：
    html = f'<h1>🔍 搜索 "{keyword}" 的结果</h1>'
    html += '<a href="/">← 返回首页</a><hr>'
    if not results:
        html += '<p>未找到相关卡片。</p>'
    else:
        for card in results:
            html += f'''
            <div style="border:1px solid #ccc; margin:10px; padding:10px; border-radius:8px;">
                <h3>{card['title']} <small>(ID: {card['id']})</small></h3>
                <p>{card['content']}</p>
            </div>
            '''
    return html

@app.route('/delete/<int:card_id>')
def delete_card(card_id):
    success = database.delete_card(card_id)
    if not success:
        return f"未找到ID为{card_id}的卡片。<a href='/'>返回首页</a>"
    return redirect(url_for('index'))

@app.route('/edit/<int:card_id>')
def edit_form(card_id):
    card = database.get_card_by_id(card_id)
    if card is None:
        return f"未找到ID为{card_id}的卡片。<a href='/'>返回首页</a>"
    return render_template('edit.html', card=card)

@app.route('/edit/<int:card_id>', methods=['POST'])
def edit_card(card_id):
    title = request.form['title'].strip()
    content = request.form['content'].strip()
    if not title or not content:
        return f"标题和内容不能为空！<a href='/edit/{card_id}'>返回</a>"
    success = database.update_card(card_id, title, content)
    if not success:
        return f"未找到ID为{card_id}的卡片。<a href='/'>返回首页</a>"
    return redirect(url_for('index'))

if __name__ == '__main__':

    # 本地开发用 debug 模式，部署时 Render 会用 gunicorn 启动
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)