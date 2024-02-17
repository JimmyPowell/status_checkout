import psutil
import requests
import time
import socket

AGENT_ID = '日本nextchat服务器'  # 假设使用主机名作为agent的唯一标识

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return {'agent_id': AGENT_ID, 'cpu_usage': cpu_usage, 'memory_usage': memory_usage}

def send_data_to_server(data):
    server_url = "http://211.159.163.132:5000/api/monitor"  # 替换为你的服务器地址
    try:
        response = requests.post(server_url, json=data)
        print(f"Data sent: {data} | Server response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {e}")

def ping_server():
    server_url = "http://211.159.163.132:5000"  # 替换为你的服务器地址
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            print("Ping successful.")
        else:
            print("Ping failed.")
    except requests.exceptions.RequestException:
        print("Ping failed.")

if __name__ == "__main__":
    while True:
        system_info = get_system_info()
        send_data_to_server(system_info)
        ping_server()  # 检查服务器的可达性
        time.sleep(10)  # 每60秒发送一次数据并ping一次服务器，根据需要调整频率