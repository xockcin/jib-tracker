# for raspberry pi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
import shutil

#browser_path = shutil.which("chromium")

options = Options()
#options.binary_location = browser_path
options.add_argument('--headless')

song_file = open("song_file.csv", "w", newline='', encoding='utf-8')
song_writer = csv.DictWriter(song_file, fieldnames=["title", "artist", "time"])

def connect():
    driver = webdriver.Chrome(options=options)
    driver.get("https://wjib.com/recently-played/")
    print("Connected to WJIB's recently played page.")
    return driver

def scrape_current_song():
    title = driver.find_element(By.CLASS_NAME, "ssiencorepl_songTitle")
    artist = driver.find_element(By.CLASS_NAME, "ssiencorepl_songArtist")
    now = time.strftime('%H:%M%p %Z on %b %d, %Y')
    return {"title" : title.text, "artist": artist.text}, {"time": now}

def record_song(song, time):
    song_writer.writerow(song | time)
    song_file.flush()

driver = connect()

current_song, current_time = scrape_current_song()

while True:
    try:    
        next_song, next_time = scrape_current_song()
    except:
        driver = connect()
        next_song, next_time = scrape_current_song()

    if next_song != current_song:
        record_song(next_song, next_time)
        print(f"New song detected: {next_song['title']} by {next_song['artist']} at {next_time['time']}")
        current_song = next_song
    
    time.sleep(60)  # Check every minute