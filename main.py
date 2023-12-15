from flask import Flask, request, jsonify, send_file
import base64
import random
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import json
import string
import os
import uuid
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()  # Install or update ChromeDriver

app = Flask(__name__)

ua_generator = UserAgent()


def generate_user_agent():
    return ua_generator.random


def generate_canvas_fingerprint(user_agent):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    with webdriver.Chrome(options=chrome_options) as browser:
        browser.execute_cdp_cmd("Network.enable", {})
        browser.execute_cdp_cmd("Network.setBypassServiceWorker", {"bypass": True})
        browser.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": True})
        browser.execute_cdp_cmd("Page.setLifecycleEventsEnabled", {"enabled": False})
        browser.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})

        fingerprint = browser.execute_script('''
            var canvas = document.createElement("canvas");
            var ctx = canvas.getContext("2d");

            // Introduce randomness
            var randomColor1 = "#" + Math.floor(Math.random()*16777215).toString(16);
            var randomColor2 = "#" + Math.floor(Math.random()*16777215).toString(16);
            var randomText = "Hello" + Math.floor(Math.random() * 100);

            ctx.textBaseline = "top";
            ctx.font = "14px 'Arial'";
            ctx.textBaseline = "alphabetic";
            ctx.fillStyle = randomColor1;
            ctx.fillRect(125, 1, 62, 20);
            ctx.fillStyle = randomColor2;
            ctx.fillText(randomText, 2, 15);

            var b64 = canvas.toDataURL().replace("data:image/png;base64,","");
            var bin = atob(b64);
            var crc = bin2hex(bin.slice(-16,-12));
            return crc;

            function bin2hex(bin){
                var hex = "";
                for(var i=0;i<bin.length;i++){
                    hex += (bin.charCodeAt(i) >>> 4).toString(16);
                    hex += (bin.charCodeAt(i) & 0xF).toString(16);
                }
                return hex;
            }
        ''')

        return fingerprint


@app.route("/canvas-fingerprint/")
def get_canvas_fingerprint():
    user_agent = request.headers.get("User-Agent", "")

    if not user_agent:
        # If no User-Agent is provided, generate a random one
        user_agent = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    # Generate the Canvas fingerprint
    fingerprint = generate_canvas_fingerprint(user_agent)

    # Generate realistic but randomized WebGL data and screen resolution
    webgl_data = {
        "vendor": f"Vendor {random.choice(['A', 'B', 'C'])}",
        "renderer": f"Renderer {random.choice(['X', 'Y', 'Z'])}",
        "version": f"Version {random.randint(1, 10)}",
        "extensions": [f"ext{i}" for i in range(1, random.randint(1, 5))]
    }
    screen_resolution = [random.randint(800, 2560), random.randint(600, 1600)]

    return jsonify({
        "user_agent": user_agent,
        "canvas_fingerprint": fingerprint,
        "webgl_data": base64.b64encode(json.dumps(webgl_data).encode()).decode(),
        "screen_resolution": screen_resolution
    })

def generate_canvas_image(user_agent, webgl_data, screen_resolution):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    try:
        webgl_data_dict = json.loads(webgl_data)
    except json.JSONDecodeError:
        webgl_data_dict = {}

    with webdriver.Chrome(options=chrome_options) as browser:
        browser.execute_cdp_cmd("Network.enable", {})
        browser.execute_cdp_cmd("Network.setBypassServiceWorker", {"bypass": True})
        browser.execute_cdp_cmd("Emulation.setScriptExecutionDisabled", {"value": True})
        browser.execute_cdp_cmd("Page.setLifecycleEventsEnabled", {"enabled": False})
        browser.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})

        # Set additional parameters for canvas fingerprinting
        browser.execute_script(f'''
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: () => {random.randint(2, 8)}
            }});
            // ... (other properties)
            navigator.plugins = [{', '.join([f"{{name: '{plugin}', description: '{random.choice(['Description A', 'Description B', 'Description C'])}', filename: '{random.choice(['plugin.dll', 'plugin.so', 'plugin.dylib'])}', version: '{random.randint(1, 10)}'}}" for plugin in ['Plugin 1', 'Plugin 2', 'Plugin 3']])}];
        ''')

        # Execute JavaScript code to generate a Canvas image and retrieve data URL
        image_data = browser.execute_script('''
            // Introduce randomness
            var randomColor1 = "#" + Math.floor(Math.random()*16777215).toString(16);
            var randomColor2 = "#" + Math.floor(Math.random()*16777215).toString(16);
            var randomText = "Hello" + Math.floor(Math.random() * 100);

            var canvas = document.createElement("canvas");
            var ctx = canvas.getContext("2d");

            ctx.textBaseline = "top";
            ctx.font = "14px 'Arial'";
            ctx.textBaseline = "alphabetic";
            ctx.fillStyle = randomColor1;
            ctx.fillRect(125, 1, 62, 20);
            ctx.fillStyle = randomColor2;
            ctx.fillText(randomText, 2, 15);

            // Include WebGL data
            var webglData = JSON.parse(arguments[0]);
            for (var key in webglData) {
                window[key] = webglData[key];
            }

            return canvas.toDataURL();
        ''', webgl_data)

    # Decode the base64 image data
    image_binary = base64.b64decode(image_data.split(',')[1])

    # Execute JavaScript code on the page to generate a Canvas image
    browser.get("about:blank")
    screenshot = browser.get_screenshot_as_png()


    return screenshot


# Update the route to return the file path
@app.route("/canvas-image/", methods=["POST"])
def get_canvas_image():
    user_agent = request.headers.get("User-Agent", "")
    webgl_data = request.json.get("webgl_data", "")
    screen_resolution = request.json.get("screen_resolution", [1920, 1080])

    image_binary = generate_canvas_image(user_agent, json.dumps(webgl_data), screen_resolution)

    # Return binary image data without JSON serialization
    return send_file(
        BytesIO(image_binary),
        mimetype="image/png",
        as_attachment=True,
        download_name="canvas_image.png"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
