from flask import Flask, request, send_file, render_template_string
from pytube import YouTube
import instaloader
import tweepy
from TikTokApi import TikTokApi
import os

app = Flask(__name__)

# Konfigurasi untuk API Twitter
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    platform = request.form['platform']
    try:
        if platform == 'youtube':
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download(filename="video.mp4")
            return send_file("video.mp4", as_attachment=True)

        elif platform == 'instagram':
            loader = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
            loader.download_post(post, target="insta_download")
            # Sesuaikan path file
            return send_file("insta_download/post.jpg", as_attachment=True)

        elif platform == 'twitter':
            tweet = twitter_api.get_status(url.split('/')[-1], tweet_mode="extended")
            media_url = tweet.extended_entities['media'][0]['video_info']['variants'][0]['url']
            # Download file video dari media_url dan return sebagai attachment
            # (Implementasi download video perlu ditambahkan)

        elif platform == 'tiktok':
            api = TikTokApi()
            video_data = api.get_video_by_url(url)
            with open("tiktok_video.mp4", "wb") as f:
                f.write(video_data)
            return send_file("tiktok_video.mp4", as_attachment=True)

        else:
            return "Platform tidak didukung!"

    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == "__main__":
    app.run(debug=True)
