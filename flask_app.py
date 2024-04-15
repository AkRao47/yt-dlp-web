from flask import Flask, render_template, request
import yt_dlp
import json
import re,os


def download_regex(input_text, localformat):
    try:
        return re.search(r'"format_id": "' + localformat + '".*?url": "(https://.*?)"', input_text, re.IGNORECASE).group(1)
    except AttributeError:
        return "notfound"

def download_url(youtube_link, format):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_link, False)
        jstring = json.dumps(info)
        return download_regex(jstring, format)

def thumbnail_regex(input_text):
    return re.search(r'.*?watch\?v=(.*?)\Z', input_text, re.IGNORECASE).group(1)


app = Flask(__name__, template_folder='./static-html/')


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/data/notfound/')
def error():
    return "Format was not found! <a href= \"{}\">Try again!</a>".format(request.host_url)


@app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return "This is a POST API, there is nothing for a GET request here..."
    if request.method == 'POST':
        if re.match(r'https://www\.youtube\.com/watch\?v=[A-Za-z0-9]+', request.form['yt_url'], re.IGNORECASE) is None:
            return "Make sure your url is in the following format:<br>https://www.youtube.com/watch?v=o-YBDTqX_ZU"
        dl360 = download_url(request.form['yt_url'], "18")
        dl720 = download_url(request.form['yt_url'], "22")
        thumbnail_link = "https://i.ytimg.com/vi/" + thumbnail_regex(request.form['yt_url']) + "/0.jpg"
        return render_template('download.html',
                               dl360=dl360,
                               dl720=dl720,
                               thumbnail_link=thumbnail_link)


if __name__ == "__main__":
    # Retrieve the port number from the PORT environment variable
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set

    # Run the Flask app with the specified host and port
    app.run(host='0.0.0.0', port=port)
