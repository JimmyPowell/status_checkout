from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 初始化数据库，创建表格
def init_db():
    conn = sqlite3.connect('system_info.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS system_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT,
        cpu_usage REAL,
        memory_usage REAL,
        last_update TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# API端点，接收来自agent的数据
@app.route('/api/monitor', methods=['POST'])
def api_monitor():
    data = request.json
    if data:
        agent_id = data.get('agent_id')
        cpu_usage = data.get('cpu_usage')
        memory_usage = data.get('memory_usage')
        last_update = datetime.now()
        conn = sqlite3.connect('system_info.db')
        c = conn.cursor()
        c.execute("INSERT INTO system_info (agent_id, cpu_usage, memory_usage, last_update) VALUES (?, ?, ?, ?)", (agent_id, cpu_usage, memory_usage, last_update))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Data received successfully"})
    else:
        return jsonify({"status": "error", "message": "No data received"}), 400

# 主页路由，渲染显示所有agent数据的页面
@app.route('/')
def index():
    return render_template('index.html')





@app.route('/api/data')
def api_data():
    conn = sqlite3.connect('system_info.db')
    c = conn.cursor()
    # 查询每个 agent_id 的最新记录
    c.execute("""
    SELECT si.agent_id, si.cpu_usage, si.memory_usage, si.last_update
    FROM system_info si
    INNER JOIN (
        SELECT agent_id, MAX(last_update) as MaxDate
        FROM system_info
        GROUP BY agent_id
    ) groupedsi ON si.agent_id = groupedsi.agent_id AND si.last_update = groupedsi.MaxDate
    ORDER BY si.last_update DESC
    """)
    agents_data = c.fetchall()
    conn.close()
    # 准备 JSON 数据
    data = [{
        'agent_id': row[0],
        'cpu_usage': row[1],
        'memory_usage': row[2],
        'last_update': row[3]
    } for row in agents_data]
    return jsonify(data)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
