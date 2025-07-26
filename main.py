import os
import streamlit as st
import requests
import socketserver
import threading
import socket

# Install streamlit if not installed (optional guard)
try:
    import streamlit
except ImportError:
    os.system("pip install streamlit")

# --- Server Configuration Fixes ---
socketserver.TCPServer.allow_reuse_address = True

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

# --- Custom Handler ---
class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Received:", self.data)

# --- Start Server ---
def execute_server(port):
    with socketserver.TCPServer(("", port), MyHandler) as httpd:
        print(f"Server running on http://localhost:{port}")
        httpd.serve_forever()

# --- Facebook Send Function ---
def send_message(token, convo_id, message):
    url = f"https://graph.facebook.com/v20.0/{convo_id}/messages"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "messaging_type": "UPDATE",
        "message": {"text": message}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text

# --- Streamlit UI ---
st.title("📩 Facebook Group Message Sender")

token = st.text_input("🔑 Page Access Token", type="password")
message = st.text_area("💬 Message to Send")

convo_id_path = "convo_id.txt"
if os.path.exists(convo_id_path):
    with open(convo_id_path, "r") as file:
        convo_id = file.read().strip()
else:
    convo_id = None
    st.warning("⚠️ 'convo_id.txt' not found!")

if st.button("🚀 Send Message"):
    if not token or not message or not convo_id:
        st.error("❌ Token, Message, or Convo ID is missing.")
    else:
        status_code, response_text = send_message(token, convo_id, message)
        if status_code == 200:
            st.success("✅ Message sent successfully!")
        else:
            st.error(f"❌ Failed to send. Status: {status_code}\n{response_text}")

# --- Start Background Server Only Once ---
if "server_started" not in st.session_state:
    st.session_state["server_started"] = True
    PORT = get_free_port()
    threading.Thread(target=execute_server, args=(PORT,), daemon=True).start()
