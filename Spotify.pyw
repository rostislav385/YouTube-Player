import tkinter as tk
from tkinter import simpledialog, messagebox
from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
import pyglet
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import webbrowser
from PIL import Image, ImageTk
import urllib.request
import io
import lyricsgenius
import re
import sys
import ctypes
import pandas as pd
import subprocess





with open("admin_root.py", "r") as file:
    admin_root_ask = file.read()
    print(int(admin_root_ask))


def run_as_admin():
    # Проверяем, запущен ли скрипт с правами администратора
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        # Если не запущен, запрашиваем права администратора
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    

if int(admin_root_ask) == 0:
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        result = messagebox.askquestion("User Agreement", "Are you sure you agree with our User Agreement?")
        if result == "yes":
            webbrowser.open_new("licence.html")
        else:
            sys.exit()

        abs_path = os.path.abspath("admin_root.py")
        if "C:" in abs_path:
            print("Fatal error")
            messagebox.showerror("Fatal Error", "Our Pathagent realized that our Programm is on the disk C:. At disk C: we need Admin root. You have to reopen this Programm with Admin Rights")
            sys.exit()
        else:
            with open("admin_root.py", "w") as file:
                root_info = "1"
                file.write(root_info)
    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
        abs_path = os.path.abspath("admin_root.py")
        if "C:" in abs_path:
            with open("admin_root.py", "w") as file:
                root_info = "2"
                file.write(root_info)
                
if int(admin_root_ask) == 1:
    print("Admin root are not needed")
if int(admin_root_ask) == 2:
    run_as_admin()




local_version = 0.3

url = "https://raw.githubusercontent.com/rostislav385/test2/main/settings.xlsx"
file_path = "settings.xlsx"

urllib.request.urlretrieve(url, file_path)

file_path = "settings.xlsx"
df = pd.read_excel(file_path)


columns_names = df.columns.tolist()
first_column_name = columns_names[0]
second_column_name = columns_names[1]

#print(first_column_name)
#print(second_column_name)

if float(local_version) == float(second_column_name):
    print("version is okay")
else:
    file_path = "update.py"
    file_path2 = "update.exe"
    if os.path.exists(file_path) or os.path.exists(file_path2):
        try:
            os.system("update.exe")
            messagebox.info("New Version", "There is a new Version, the app will be reinstalled")
        except:
            try:
                os.system("update.py")
                messagebox.info("New Version", "There is a new Version, the app will be reinstalled")
            except:
                messagebox.showerror("Version Error", "There is an Upate of your app, pls download it. The app will be closed")
                sys.exit()



class YoutubePlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Player")

        self.current_volume = 0.5  # Default volume level


        # Frame for video thumbnail
        self.video_thumbnail_frame = tk.Frame(self.root, width=400, bg='lightgrey')
        self.video_thumbnail_frame.place(x=500, y=100)  # Установка координат x и y

        self.video_thumbnail_label = tk.Label(self.video_thumbnail_frame)
        self.video_thumbnail_label.configure(width=300, height=200) 
        self.video_thumbnail_label.pack(padx=5, pady=5)


        # Создание фрейма для текста песен
        self.text_songs_frame = tk.Frame(self.root, width=600, height=200, bg='lightgrey')
        self.text_songs_frame.pack_propagate(False)
        self.text_songs_frame.place(x=500, y=350)

        # Создание текстового поля для отображения текста песни
        self.song_text = tk.Text(self.text_songs_frame, wrap='word', state='disabled')
        self.song_text.pack(fill='both', expand=True)

        # Frame for menu
        self.menu_frame = tk.Frame(self.root, bg='lightgrey')
        self.menu_frame.pack(side='top', fill='x')

        self.search_entry = tk.Entry(self.menu_frame)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        self.search_button = tk.Button(self.menu_frame, text="Search", command=self.search)
        self.search_button.pack(side='left', padx=5, pady=5)

        self.settings_button = tk.Button(self.menu_frame, text="⚙", command=self.open_settings)
        #self.settings_button.pack(side='left', padx=5)

        # Settings button with dropdown menu
        self.settings_button = tk.Menubutton(self.menu_frame, text="⚙")
        self.settings_button.pack(side='left', padx=5)
        self.settings_menu = tk.Menu(self.settings_button, tearoff=0)
        self.settings_menu.add_command(label="Refresh", command=self.refresh_playlist)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Import from Spotify", command=self.import_from_spotify)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Download Playlist", command=self.download_your_playlist)
        self.settings_button.config(menu=self.settings_menu)
        self.settings_button.pack(side='left', padx=5)

        # Frame for playlist
        self.playlist_frame = tk.Frame(self.root, width=200, bg='lightgrey')
        self.playlist_frame.pack(side='left', fill='y')

        self.playlist_listbox = tk.Listbox(self.playlist_frame)
        self.playlist_listbox.pack(fill='both', expand=True)
        self.playlist_listbox.bind("<<ListboxSelect>>", self.load_songs)

        # Add playlist button
        self.add_playlist_button = tk.Button(self.playlist_frame, text="+", command=self.add_playlist, width=3)
        self.add_playlist_button.pack(side='left', padx=(5, 2), pady=5)
        self.delete_playlist_button = tk.Button(self.playlist_frame, text="-", command=self.delete_playlist, width=3)
        self.delete_playlist_button.pack(side='left', padx=(2, 5), pady=5)

        # Frame for songs
        self.songs_frame = tk.Frame(self.root, bg='white')
        self.songs_frame.pack(side='left', fill='both', expand=False, padx=5, pady=5)

        self.songs_listbox = tk.Listbox(self.songs_frame, width=60)
        self.songs_listbox.pack(fill='both', expand=True)
        self.songs_listbox.bind("<<ListboxSelect>>", self.play_selected_song)

        # Frame for song information
        self.info_frame = tk.Frame(self.root, width=200, bg='lightgrey')
        self.info_frame.pack(side='right', fill='y')

        self.info_label = tk.Label(self.info_frame, text="Song Information", bg='lightgrey', wraplength=200, anchor='w')
        self.info_label.pack(fill='both', expand=False)

        self.add_to_playlist_button = tk.Button(self.info_frame, text="Add to Playlist", command=self.add_to_playlist)
        self.add_to_playlist_button.pack(fill='both', expand=False)
        self.remove_song_button = tk.Button(self.songs_frame, text="Remove Song", command=self.remove_song)
        self.remove_song_button.pack(side='bottom', padx=5, pady=5)
        self.remove_song_button = tk.Button(self.songs_frame, text="Edit song name", command=self.edit_song_name)
        self.remove_song_button.pack(side='bottom', padx=5, pady=5)

        # Link to video
        self.link_label = tk.Label(self.info_frame, text="Video Link:", fg="blue", cursor="hand2")
        self.link_label.pack(fill='both', expand=True)
        self.link_label.bind("<Button-1>", self.open_link)

        # Frame for control buttons
        self.controls_frame = tk.Frame(self.root, bg='lightgrey')
        self.controls_frame.pack(side='bottom', fill='x')

        self.prev_button = tk.Button(self.controls_frame, text="⏮", command=self.prev_song)
        self.prev_button.pack(side='left', padx=5, pady=5)

        self.play_pause_button = tk.Button(self.controls_frame, text="⏯", command=self.play_pause)
        self.play_pause_button.pack(side='left', padx=5, pady=5)

        self.next_button = tk.Button(self.controls_frame, text="⏭", command=self.next_song)
        self.next_button.pack(side='left', padx=5, pady=5)

        self.volume_slider = tk.Scale(self.controls_frame, from_=0, to=1, resolution=0.01, orient='horizontal',
                                      label='Volume', command=self.change_volume)
        self.volume_slider.set(self.current_volume)
        self.volume_slider.pack(side='right', padx=5, pady=5)
        self.volume_slider.bind("<ButtonRelease-1>", self.save_volume)

        self.load_volume()


        # Load playlists
        self.playlists = self.load_playlists()
        self.update_playlist_listbox()
        
        # Шкала для отображения прогресса воспроизведения
        self.progress_scale = tk.Scale(self.controls_frame, from_=0, to=100, orient='horizontal', highlightthickness=0, showvalue=False)
        self.progress_scale.pack(side='right', fill='x', padx=5, pady=5)
        self.progress_scale.bind("<ButtonRelease-1>", lambda event: self.change_progress(self.progress_scale.get()))

        # Label для отображения текущей позиции трека и его длительности
        self.time_label = tk.Label(self.controls_frame, text="0:00 / 0:00")
        self.time_label.pack(side='left', padx=5, pady=5)


        # Обновление шкалы прогресса воспроизведения и времени
        self.update_progress()
        self.loading = False
        self.invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ';']
        self.genius = lyricsgenius.Genius("fJZ0ZyaAwHfYU7ETXPqoetCvgFh_4kugVvR8Pak5g6WxFuuDUr2Rs5_QM4Hi10U_")


        # Load songs
        if self.playlists:
            self.load_songs(None)
    def download_is_confermed(self):
        current_playlist = self.playlist_listbox.get(tk.ACTIVE)
        with open(f"config_songs_{current_playlist}.txt", "r+") as file:
            content = file.read()
            for invalid_char in self.invalid_chars:
                if invalid_char in content:
                    print("invalid CONTENT")
                    messagebox.showerror("Fatal Error", "Some of songs has invalid CONTENT. Downloading will be returned. All songs with invalid symbols will be renamed")
                    print(content)
                    content = self.sanitize_filename(content)
                    with open(f"config_songs_{current_playlist}.txt", "w") as file:  # Открываем файл для записи
                        file.write(content)  # Перезаписываем файл с обработанным содержимым
                    for invalid_char in self.invalid_chars:
                        if invalid_char in content:
                            print("invalid CONTENT")
                            messagebox.showerror("Fatal Error", "Some of songs has invalid CONTENT. Downloading will be returned. We can`t help you. Rename song by your own")
                            return
                        else:
                            messagebox.showinfo("Info", "All invalid CONTENT was deleted. The app will be refreshed")
                            self.refresh_playlist()


        with open(f"config_songs_{current_playlist}.txt", "r", encoding="cp1251", errors='replace') as file:
            file_content = file.read()
            print(file_content)

            lines = file_content.split('\n')
            print(lines)

            for line in lines: 
                if line.strip():  # Проверка на непустую строку
                    query = line
                    results = VideosSearch(query, limit=1).result()
                    if results:
                        try:
                            video_url = f"https://www.youtube.com/watch?v={results['result'][0]['id']}"
                            if os.path.exists(f"./songs/{current_playlist}/{line}.mp3"):
                                print(f"{line}.mp3 already exists, I pass it thought")
                                continue
                            yt = YouTube(video_url)
                            stream = yt.streams.filter(only_audio=True).first()
                            stream.download(output_path=f"./songs/{current_playlist}", filename=f"{line}.mp3")
                            print(f"{line}.mp3 is succesfuly downloaded")
                        except Exception as e:
                            messagebox.showwarning("Warning", f"{line} can`t be downloaded because of the 'Age restriction', song won`t be donwnloaded, we are sorry about that. All question to YouTube Staff")
                    else:
                        print("Video not found")

    def edit_song_name(self):
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        if not selected_playlist:
            messagebox.showwarning("Warning", "No playlist selected.")
            return

        selected_song_index = self.songs_listbox.curselection()
        if not selected_song_index:
            messagebox.showwarning("Warning", "No song selected.")
            return

        selected_index = selected_song_index[0]
        song_name = self.songs_listbox.get(selected_index)

        new_name = simpledialog.askstring("Edit Song Name", f"Enter new name for '{song_name}':")
        if new_name is None:
            # User clicked cancel
            return

        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to change '{song_name}' to '{new_name}'?")
        if confirmation:
            songs_file = f"config_songs_{selected_playlist}.txt"
            if os.path.exists(songs_file):
                with open(songs_file, "r", encoding="cp1251", errors='replace') as file:
                    songs = file.read().splitlines()

                songs[selected_index] = new_name

                with open(songs_file, "w", encoding="cp1251", errors='replace') as file:
                    file.write("\n".join(songs))

            self.songs_listbox.delete(selected_index)
            self.songs_listbox.insert(selected_index, new_name)
            messagebox.showinfo("Info", f"Song '{song_name}' has been changed to '{new_name}' in the playlist.")


    def sanitize_filename(self, song_name_remake):
        # Заменяем недопустимые символы
        return re.sub(r'[<>:"/\\|?*]', '', song_name_remake)
    def download_your_playlist(self):
        # Получить текущее имя выбранного плейлиста
        current_playlist = self.playlist_listbox.get(tk.ACTIVE)

        # Отобразить диалоговое окно с подтверждением удаления плейлиста
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to download the playlist '{current_playlist}'?")

        if confirmation:
            self.download_is_confermed()
    def search_lyrics(self, song_title, artist):
        try:
            if "(" in song_title and ")" in song_title:
                artist = re.sub(r'\([^()]*\)', '', song_title)
            else:
                artist = song_title
            query = f"{artist}"
            song = self.genius.search_song(query)
            if song:
                return song.lyrics
            else:
                return None
        except Exception as e:
            print("Error:", e)
            return None
    def load_song_lyrics(self, lyrics):
        # Очистить текстовое поле перед загрузкой нового текста
        self.song_text.config(state='normal')
        self.song_text.delete('1.0', tk.END)
        # Загрузить текст песни в текстовое поле
        self.song_text.insert(tk.END, lyrics)
        # Заблокировать текстовое поле от редактирования
        self.song_text.config(state='disabled')
    def open_link(self, event):
        print("open_link")
        selected_song_title = self.info_label.cget("text")
        query = selected_song_title
        results = VideosSearch(query, limit=1).result()
        if results:
            try:
                video_url = f"https://www.youtube.com/watch?v={results['result'][0]['id']}"
                webbrowser.open(video_url)
            except Exception as e:
                print(e)
                if e != "":
                    messagebox.showerror("Fatal Error", f"Song '{query}' can`t be played because of the 'Age restriction. Song will be skiped'")
                    self.next_song()
        else:
            messagebox.showerror("Error", "Video not found!")
    def change_progress(self, position):
        print("change_progress")
        # position - значение, которое представляет позицию ползунка
        if hasattr(self, 'player') and self.player.source:
            duration = self.music.duration
            new_time = (position / 100) * duration
            self.player.seek(new_time)
    def load_video_thumbnail(self, video_url):
        print("load_video_thumbnail")
        video_id = video_url.split("v=")[1]
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        print("Trying to load thumbnail from URL:", thumbnail_url)  # Добавить эту строку для вывода в консоль
        try:
            image_data = urllib.request.urlopen(thumbnail_url).read()
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((100, 100))  # Размер изображения можно настроить по вашему желанию
            photo = ImageTk.PhotoImage(image)

            image = Image.open(io.BytesIO(image_data))
            width, height = image.size
            # Рассчитаем новые размеры изображения с соотношением сторон 300x200
            if width > height:
                new_width = 300
                new_height = int(height * (300 / width))
            else:
                new_height = 200
                new_width = int(width * (200 / height))
            # Изменение размеров изображения с использованием LANCZOS
            image = image.resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Отобразите изображение на вашем интерфейсе
            self.video_thumbnail_label.config(image=photo, width=300, height=200)
            self.video_thumbnail_label.image = photo
        except urllib.error.HTTPError as e:
            print("HTTP Error:", e)
    def open_settings(self):
        print("open_settings")
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        # Frame for Spotify import
        spotify_import_frame = tk.Frame(settings_window, bg='white')
        spotify_import_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Label and Entry for playlist URL
        url_label = tk.Label(spotify_import_frame, text="Playlist URL:")
        url_label.pack(pady=(10, 0))
        self.playlist_url_entry = tk.Entry(spotify_import_frame)
        self.playlist_url_entry.pack(fill='x', padx=5)

        # Buttons for import and cancel
        button_frame = tk.Frame(settings_window, bg='white')
        button_frame.pack(pady=(10, 0))
        import_button = tk.Button(button_frame, text="Import", command=self.import_from_spotify)
        import_button.pack(side='left', padx=5)
        cancel_button = tk.Button(button_frame, text="Cancel", command=settings_window.destroy)
        cancel_button.pack(side='left', padx=5)

    def import_from_spotify(self):
        print("import_from_spotify")
        playlist_url = simpledialog.askstring("Import from Spotify", "Enter the Spotify playlist URL:")
        if playlist_url:
            # Process the playlist URL and add it to the application
            self.process_spotify_playlist(playlist_url)
        else:
            messagebox.showwarning("Warning", "Please enter a playlist URL")
    def process_spotify_playlist(self, playlist_url):
        # Placeholder function for processing Spotify playlist URL
        try:
            print("process_spotify_playlist")
            songs = self.get_playlist_tracks(playlist_url)

            # Вывод списка песен
            if songs:
                for song in songs:
                    print(song)
            else:
                print("Не удалось получить список песен из плейлиста.")
        except:
            messagebox.showerror("Song Error", "Songs list can`t be donwnloaded. Maybe some of songs names containes invalid Symbols")
    def replace_non_cp1251_chars(self, text):
        # Пробуем закодировать строку в cp1251 и заменяем символы, которые не могут быть закодированы, на пустую строку
        encoded_text = text.encode('cp1251', errors='replace')
        # Декодируем обратно в строку
        decoded_text = encoded_text.decode('cp1251')
        print(decoded_text)
        return decoded_text
    def get_playlist_tracks(self, playlist_url):
        # Инициализация клиента spotipy
        client_credentials_manager = SpotifyClientCredentials(client_id='d55d131aaf074f36a6f965049981d1c6', client_secret='4e64a15f0fb4435399de21b019d41a12')
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Извлечение идентификатора плейлиста из ссылки
        playlist_id = playlist_url.split('/')[-1].split('?')[0]

        try:
            # Получение информации о плейлисте
            playlist_info = sp.playlist(playlist_id)

            # Извлечение названия плейлиста
            playlist_name = playlist_info['name']

            # Создание списка для хранения названий песен и исполнителей
            song_list = []

            # Начальная страница треков
            tracks = playlist_info['tracks']
            while tracks:
                for item in tracks['items']:
                    if item is None or item['track'] is None:
                        continue
                    track = item['track']
                    track_name = track.get('name', 'Unknown')
                    artists = track.get('artists', [])
                    artist_names = ', '.join([artist.get('name', 'Unknown') for artist in artists])
                    song_list.append(f"{track_name} - {artist_names}")

                # Проверка, есть ли следующая страница треков
                tracks = sp.next(tracks) if tracks['next'] else None

            try:
                for songs in song_list:
                    encoded_text = songs.encode('cp1251')
                    decoded_text = encoded_text.decode('cp1251')
            except:
                messagebox.showerror("Song Error", "Some your song has problems with 'cp1251', we will try to fix it. All unsupportaple Symbols will be deleted")

            # Запись информации в файл плейлиста
            with open("config_playlists.txt", "a", encoding="cp1251", errors='replace') as file:
                file.write(f"{playlist_name}\n")

            # Запись треков в файл плейлиста
            with open(f"config_songs_{playlist_name}.txt", "w", encoding="cp1251", errors='replace') as file:
                for song in song_list:
                    file.write(f"{song}\n")

            return song_list
        except Exception as e:
            print("Ошибка при получении информации о плейлисте:", e)
            messagebox.showerror("Song Error", "Songs list can`t be donwnloaded. Maybe some of songs names containes invalid Symbols")
            return None


    def load_volume(self):
        print("load_volume")
        if os.path.exists("config_voice.txt"):
            with open("config_voice.txt", "r", encoding="cp1251", errors='replace') as file:
                volume = file.readline().strip()
                if volume:
                    self.current_volume = float(volume)
                    if hasattr(self, 'player'):
                        self.player.volume = self.current_volume
                    self.volume_slider.set(self.current_volume)

    def save_volume(self, event=None):
        print("save_volume")
        with open("config_voice.txt", "w", encoding="cp1251", errors='replace') as file:
            file.write(str(self.current_volume))

    def change_volume(self, val):
        print("change_volume")
        self.current_volume = float(val)
        if hasattr(self, 'player'):
            self.player.volume = self.current_volume
        self.save_volume()  # Сохранение текущей громкости при ее изменении

    def search(self):
        print("search")
        self.loading = False
        query = self.search_entry.get()
        results = VideosSearch(query, limit=1).result()
        if results:
            video_url = f"https://www.youtube.com/watch?v={results['result'][0]['id']}"
            try:
                self.download_audio(video_url)
                self.info_label.config(text=results['result'][0]['title'])
            except Exception as e:
                print(e)
                if e != "":
                    messagebox.showerror("Fatal Error", f"Song '{query}' can`t be played because of the 'Age restriction. Song will be skiped'")
                    self.next_song()
        else:
            print("Video not found")

    def download_audio(self, video_url):
        print("download_audio")
        self.load_video_thumbnail(video_url)
        # Delete the previously downloaded file if it exists
        if self.loading:
            return
        self.loading = True
        if os.path.exists("audio_temp.mp3"):
            os.remove("audio_temp.mp3")

        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=".", filename="audio_temp.mp3")

        # Wait for the file to be fully saved
        #time.sleep(2)


        self.play_audio()
    def play_audio(self):
        print("play_audio")
        # Check if the file exists
        if not self.loading:
            return
        if os.path.exists("audio_temp.mp3"):
            self.music = pyglet.media.load("audio_temp.mp3", streaming=False)
            self.player = pyglet.media.Player()
            self.player.volume = self.current_volume
            self.player.queue(self.music)
            self.player.play()
            pyglet.clock.schedule_once(self.stop_music, self.music.duration)

    def stop_music(self, dt):
        print("stop_music")
        if hasattr(self, 'player'):
            self.player.pause()
            if self.player.source:
                self.loading = False  # После остановки сбрасываем флаг загрузки и воспроизведения
                self.next_song()

    def load_songs(self, event):
        print("load_songs")
        #self.loading = False
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        self.songs_listbox.delete(0, tk.END)
        if selected_playlist:
            songs_file = f"config_songs_{selected_playlist}.txt"
            if os.path.exists(songs_file):
                try:
                    with open(songs_file, "r", encoding="cp1251", errors='replace') as file:
                        songs = file.read().splitlines()
                    for song in songs:
                        self.songs_listbox.insert(tk.END, song)
                except UnicodeDecodeError as e:
                    print(f"Ошибка при декодировании файла: {e}")

    def play_selected_song(self, event):
        print("play_selected_song")
        self.loading = False
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        print(selected_playlist)
        selected_song_index = self.songs_listbox.curselection()
        print(selected_song_index)
        if selected_song_index:
            selected_index = selected_song_index[0]
            songs_file = f"config_songs_{selected_playlist}.txt"
            if os.path.exists(songs_file):
                with open(songs_file, "r", encoding="cp1251", errors='replace') as file:
                    songs = file.read().splitlines()
                selected_song_title = songs[selected_index]
                self.info_label.config(text=selected_song_title)
                song_title = selected_song_title
                artist = ""
                song_lyrics = self.search_lyrics(song_title, artist)  # Добавлено self здесь
                if song_lyrics:
                    self.load_song_lyrics(song_lyrics)
                self.download_audio_by_title(selected_song_title)



    def play_pause(self):
        print("play_pause")
        if hasattr(self, 'player'):
            if self.player.playing:
                self.player.pause()
            else:
                self.player.play()

    def next_song(self):
        print("next_song")
        self.loading = False
        self.player.pause()
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        current_song_index = self.songs_listbox.curselection()
        if current_song_index:
            current_index = current_song_index[0]
            songs_file = f"config_songs_{selected_playlist}.txt"
            if os.path.exists(songs_file):
                with open(songs_file, "r", encoding="cp1251", errors='replace') as file:
                    songs = file.read().splitlines()
                if current_index == len(songs) - 1:
                    next_song_index = 0  # Если текущая песня последняя, играем первую
                else:
                    next_song_index = current_index + 1
                next_song_title = songs[next_song_index]
                self.songs_listbox.selection_clear(0, tk.END)
                self.songs_listbox.select_set(next_song_index)
                self.info_label.config(text=next_song_title)
                self.download_audio_by_title(next_song_title)

                try:
                    if "(" in next_song_title and ")" in next_song_title:
                        artist = re.sub(r'\([^()]*\)', '', next_song_title)
                    else:
                        artist = next_song_title
                    query = f"{artist}"
                    song = self.genius.search_song(query)
                    if song:
                        self.song_text.config(state='normal')
                        self.song_text.delete('1.0', tk.END)
                        # Загрузить текст песни в текстовое поле
                        self.song_text.insert(tk.END, song.lyrics)  # Используем song.lyrics для получения полного текста песни
                        # Заблокировать текстовое поле от редактирования
                        self.song_text.config(state='disabled')
                    else:
                        return None
                except Exception as e:
                    print("Error:", e)
                    return None

    def prev_song(self):
        print("prev_song")
        self.loading = False
        self.player.pause()
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        current_song_index = self.songs_listbox.curselection()
        if current_song_index:
            current_index = current_song_index[0]
            songs_file = f"config_songs_{selected_playlist}.txt"
            if os.path.exists(songs_file):
                with open(songs_file, "r", encoding="cp1251", errors='replace') as file:
                    songs = file.read().splitlines()
                if current_index == 0:
                    prev_song_index = len(songs) - 1  # Если текущая песня первая, играем последнюю
                else:
                    prev_song_index = current_index - 1
                prev_song_title = songs[prev_song_index]
                self.songs_listbox.selection_clear(0, tk.END)
                self.songs_listbox.select_set(prev_song_index)
                self.info_label.config(text=prev_song_title)
                self.download_audio_by_title(prev_song_title)


                try:
                    if "(" in prev_song_title and ")" in prev_song_title:
                        artist = re.sub(r'\([^()]*\)', '', prev_song_title)
                    else:
                        artist = prev_song_title
                    query = f"{artist}"
                    song = self.genius.search_song(query)
                    if song:
                        self.song_text.config(state='normal')
                        self.song_text.delete('1.0', tk.END)
                        # Загрузить текст песни в текстовое поле
                        self.song_text.insert(tk.END, song.lyrics)  # Используем song.lyrics для получения полного текста песни
                        # Заблокировать текстовое поле от редактирования
                        self.song_text.config(state='disabled')
                    else:
                        return None
                except Exception as e:
                    print("Error:", e)
                    return None

                    
    def play_audio_from_file(self, file_path):
        print("play_audio_from_file")
        if os.path.exists(file_path):
            self.music = pyglet.media.load(file_path, streaming=False)
            self.player = pyglet.media.Player()
            self.player.volume = self.current_volume
            self.player.queue(self.music)
            self.player.play()
            pyglet.clock.schedule_once(self.stop_music, self.music.duration)

    def download_audio_by_title(self, song_title):
        print("download_audio_by_title")
        print(self.loading)
        current_playlist = self.playlist_listbox.get(tk.ACTIVE)
        if self.loading == True:
            return
        query = song_title
        results = VideosSearch(query, limit=1).result()
        if results:
            try:
                video_url = f"https://www.youtube.com/watch?v={results['result'][0]['id']}"
                # Проверяем, существует ли файл уже в папке плейлиста
                if os.path.exists(f"./songs/{current_playlist}/{song_title}.mp3"):
                    # Если файл существует, запускаем его
                    self.play_audio_from_file(f"./songs/{current_playlist}/{song_title}.mp3")
                    self.load_video_thumbnail(video_url)
                else:
                    # Если файл не существует, загружаем его
                    self.download_audio(video_url)
                    self.info_label.config(text=results['result'][0]['title'])
            except Exception as e:
                print("Error:", e)
                if e != "":
                    messagebox.showerror("Fatal Error", f"Song '{song_title}' can`t be played because of the 'Age restriction. Song will be skiped'")
                    self.next_song()
        else:
            print("Video not found")

    def add_to_playlist(self):
        print("add_to_playlist")
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        if selected_playlist:
            song_title = self.info_label.cget("text")
            songs_file = f"config_songs_{selected_playlist}.txt"
            with open(songs_file, "a", encoding="cp1251", errors='replace') as file:
                file.write("\n" + song_title + "\n")  # Добавляем символ новой строки после каждой записи

            with open(songs_file, "r", encoding="cp1251", errors='replace') as file:
                lines = file.readlines()
        
            filtered_lines = [line for line in lines if line.strip()]
        
            # Перезаписываем файл без пустых строк
            with open(songs_file, "w", encoding="cp1251", errors='replace') as file:
                file.writelines(filtered_lines)
            self.load_songs(None)
    def remove_song(self):
        print("remove_song")
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        if not selected_playlist:
            messagebox.showwarning("Warning", "No playlist selected.")
            return

        selected_song_index = self.songs_listbox.curselection()
        if not selected_song_index:
            messagebox.showwarning("Warning", "No song selected.")
            return

        selected_index = selected_song_index[0]
        song_name = self.songs_listbox.get(selected_index)

        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete '{song_name}'?")
        if confirmation:
            songs_file = f"config_songs_{selected_playlist}.txt"
            if os.path.exists(songs_file):
                with open(songs_file, "r", encoding="cp1251", errors='replace') as file:
                    songs = file.read().splitlines()

                songs.pop(selected_index)

                with open(songs_file, "w", encoding="cp1251", errors='replace') as file:
                    file.write("\n".join(songs))
                with open(songs_file, "a", encoding="cp1251", errors='replace') as file:
                    file.write("\n")

            self.songs_listbox.delete(selected_index)
            messagebox.showinfo("Info", f"Song '{song_name}' has been deleted from the playlist.")


    def delete_playlist(self):
        print("delete_playlist")
        selected_playlist = self.playlist_listbox.get(tk.ACTIVE)
        if selected_playlist:
            confirmation = tk.messagebox.askyesno("Confirmation", f"Are you sure you want to delete the playlist '{selected_playlist}'?")
            if confirmation:
                self.playlists.remove(selected_playlist)
                self.update_playlist_listbox()
                self.save_playlists()
                # Также нужно удалить файл с песнями этого плейлиста, если он существует
                songs_file = f"config_songs_{selected_playlist}.txt"
                if os.path.exists(songs_file):
                    os.remove(songs_file)

    def add_playlist(self):
        print("add_playlist")
        playlist_name = simpledialog.askstring("Create Playlist", "Enter the name of the new playlist:",
                                               parent=self.root)
        if playlist_name:
            self.playlists.append(playlist_name)
            self.update_playlist_listbox()
            self.save_playlists()

    def load_playlists(self):
        print("load_playlists")
        if os.path.exists("config_playlists.txt"):
            with open("config_playlists.txt", "r", encoding="cp1251", errors='replace') as file:
                playlists = file.read().splitlines()
            return playlists
        else:
            return []

    def save_playlists(self):
        print("save_playlists")
        with open("config_playlists.txt", "w", encoding="cp1251", errors='replace') as file:
            for playlist in self.playlists:
                file.write(playlist + "\n")

    def update_playlist_listbox(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.playlists:
            self.playlist_listbox.insert(tk.END, playlist)
            
    def refresh_playlist(self):
        print("refresh_playlist")
        # Placeholder for refresh functionality
        python = sys.executable
        os.execl(python, python, *sys.argv)
    

    def update_progress(self):
        #print("update_progress")
        # Получение текущей позиции и длительности трека
        if hasattr(self, 'player') and self.player.source:
            current_time = self.player.time
            duration = self.music.duration
            
            # Проверка, если время проигрывания трека превысило его длительность
            if current_time >= duration:
                self.next_song()
            
            # Преобразование времени в формат "мм:сс"
            current_time_str = time.strftime('%M:%S', time.gmtime(current_time))
            duration_str = time.strftime('%M:%S', time.gmtime(duration))
            
            # Обновление Label для отображения текущей позиции трека и его длительности
            self.time_label.config(text=f"{current_time_str} / {duration_str}")
            
            # Обновление шкалы прогресса воспроизведения
            progress_percent = (current_time / duration) * 100
            self.progress_scale.set(progress_percent)
        
        # Планирование следующего обновления через 100 миллисекунд
        self.root.after(100, self.update_progress)


if __name__ == "__main__":
    if int(admin_root_ask) == 2:
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            run_as_admin()
    root = tk.Tk()
    root.geometry("1300x600")
    app = YoutubePlayerApp(root)
    pyglet.app.event_loop.has_exit = lambda: True
    root.mainloop()
