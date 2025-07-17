import os
import streamlit as st
import requests
import socketserver
import threading

# Install streamlit if not installed (optional guard)
try:
    import streamlit
except ImportError:
    os.system("pip install streamlit")

# Custom server handler
class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Received:", self.data)

# Function to get free port (fixed to 5078)
PORT = 5078

def execute_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server running on http://localhost:{PORT}")
        httpd.serve_forever()

# Function to send message
def send_message(token, convo_id, message):
    url = f"https://graph.facebook.com/v20.0/{convo_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "messaging_type": "UPDATE",
        "message": {"text": message}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text

# UI via Streamlit
st.title("📩 Facebook Group Message Sender")

token = st.text_input("🔑 Page Access Token", type="password")
message = st.text_area("💬 Message to Send")

# Read convo_id from file (make sure this file exists)
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

# Start background server
threading.Thread(target=execute_server, daemon=True).start()
