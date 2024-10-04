from flask import Flask, render_template

app = Flask(__name__)

from flask import Flask, render_template, request, redirect, send_file
import yt_dlp
import os

app = Flask(__name__)

# Pasta de downloads
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Função para baixar o vídeo ou áudio
def download_video(url, download_type):
    ydl_opts = {}
    if download_type == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:  # video
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if download_type == "audio":
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        return filename
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/tools", methods=["GET", "POST"])
def tools():
    if request.method == "POST":
        url = request.form["url"]
        download_type = request.form["type"]
        try:
            filepath = download_video(url, download_type)
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return str(e)
    return render_template("tools.html")




@app.route("/videos")
def videos():
    return render_template("videos.html")
@app.route("/gogos")
def gogos():
    return render_template("gogos.html")

@app.route("/download")
def downloads():
    return render_template("download.html")

if __name__ == "__main__":
    app.run(debug=True)
