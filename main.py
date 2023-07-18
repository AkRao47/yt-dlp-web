from flask import Flask, render_template, request
import yt_dlp
import json
import re


def download_regex(input_text, localformat):
    try:
        return re.search(r'"format_id": "' + localformat + '".*?url": "(https://.*?)"', input_text, re.IGNORECASE).group(1)
    except AttributeError:
        return False


def thumbnail_regex(input_text):
    return re.search(r'.*?watch\?v=(.*?)\Z', input_text, re.IGNORECASE).group(1)


app = Flask(__name__, template_folder='./static-html/')


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/data/False')
def error():
    return "Format was not found! <a href= \"{}\">Try again!</a>".format(request.host_url)


@app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return "This is a POST API, there is nothing for a GET request here..."
    if request.method == 'POST':
        if re.match(r'https://www\.youtube\.com/watch\?v=[A-Za-z0-9]+', request.form['yt_url'], re.IGNORECASE) is None:
            return "Make sure your url is in the following format:<br>https://www.youtube.com/watch?v=CuBm69OolMk"
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.form['yt_url'], False)
            jstring = json.dumps(info)
            final_link = download_regex(jstring, request.form['format'])
            thumbnail_link = "https://i.ytimg.com/vi/" + thumbnail_regex(request.form['yt_url']) + "/0.jpg"
            if final_link is False or final_link is None:
                error = "Format not found! Make sure you chose a format that exists on the video!\nMade by SamzyDev"
            else:
                error = "Made by SamzyDev"
        match (request.form['format']):
            case '22':
                send_format = "Video + Audio (720p)"
            case '137':
                send_format = "Video + Audio (1080p)"
            case '140':
                send_format = "Audio Only (M4A)"
            case '251':
                send_format = "Audio Only (WEBM)"
            case _:
                send_format = "Unknown Format"

        return render_template('download.html',
                               download_link=final_link,
                               format=send_format,
                               error=error,
                               thumbnail_link=thumbnail_link)


app.run(host='0.0.0.0', port=80)
