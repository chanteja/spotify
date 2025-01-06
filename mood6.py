import webbrowser
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import speech_recognition as sr
import pyttsx3  # Text-to-speech library

# Spotify credentials
SPOTIPY_CLIENT_ID = '95c6413b46b84287b8194087205a7f12'
SPOTIPY_CLIENT_SECRET = '9acbf9035e0a4fadae5db1febbf822e5'

# List of available moods and languages
moods_list = ["happy", "sad", "relaxed", "energetic", "romantic", "anxious", "angry", "motivated", "calm", "nostalgic", "dance"]
languages_list = ["English", "Hindi", "Telugu", "Tamil", "Malayalam"]

# Define a dictionary of moods with corresponding Spotify search queries
spotify_queries = {
    "happy": {
        "English": "happy music",
        "Hindi": "happy Hindi music",
        "Telugu": "happy Telugu music",
        "Tamil": "happy Tamil music",
        "Malayalam": "happy Malayalam music"
    },
    "sad": {
        "English": "sad music",
        "Hindi": "sad Hindi music",
        "Telugu": "sad Telugu music",
        "Tamil": "sad Tamil music",
        "Malayalam": "sad Malayalam music"
    },
    "relaxed": {
        "English": "relaxed music",
        "Hindi": "relaxed Hindi music",
        "Telugu": "relaxed Telugu music",
        "Tamil": "relaxed Tamil music",
        "Malayalam": "relaxed Malayalam music"
    },
    "energetic": {
        "English": "energetic music",
        "Hindi": "energetic Hindi music",
        "Telugu": "energetic Telugu music",
        "Tamil": "energetic Tamil music",
        "Malayalam": "energetic Malayalam music"
    },
    "romantic": {
        "English": "romantic music",
        "Hindi": "romantic Hindi music",
        "Telugu": "romantic Telugu music",
        "Tamil": "romantic Tamil music",
        "Malayalam": "romantic Malayalam music"
    },
    "anxious": {
        "English": "anxious music",
        "Hindi": "anxious Hindi music",
        "Telugu": "anxious Telugu music",
        "Tamil": "anxious Tamil music",
        "Malayalam": "anxious Malayalam music"
    },
    "angry": {
        "English": "angry music",
        "Hindi": "angry Hindi music",
        "Telugu": "angry Telugu music",
        "Tamil": "angry Tamil music",
        "Malayalam": "angry Malayalam music"
    },
    "motivated": {
        "English": "motivated music",
        "Hindi": "motivated Hindi music",
        "Telugu": "motivated Telugu music",
        "Tamil": "motivated Tamil music",
        "Malayalam": "motivated Malayalam music"
    },
    "calm": {
        "English": "calm music",
        "Hindi": "calm Hindi music",
        "Telugu": "calm Telugu music",
        "Tamil": "calm Tamil music",
        "Malayalam": "calm Malayalam music"
    },
    "nostalgic": {
        "English": "nostalgic music",
        "Hindi": "nostalgic Hindi music",
        "Telugu": "nostalgic Telugu music",
        "Tamil": "nostalgic Tamil music",
        "Malayalam": "nostalgic Malayalam music"
    },
    "dance": {
        "English": "dance music",
        "Hindi": "dance Hindi music",
        "Telugu": "dance Telugu music",
        "Tamil": "dance Tamil music",
        "Malayalam": "dance Malayalam music"
    }
}

# Define language-specific TTS voices
voice_language_map = {
    "English": "english",
    "Hindi": "hindi",
    "Telugu": "telugu",
    "Tamil": "tamil",
    "Malayalam": "malayalam"
}

# Function to get the TTS engine for the selected language
def get_tts_engine(language):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Choose voice based on the language
    lang_voice = voice_language_map.get(language, "english")
    for voice in voices:
        if lang_voice in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    return engine

def announce(message, language):
    engine = get_tts_engine(language)
    engine.say(message)
    engine.runAndWait()

def search_spotify(query):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET
        ))
        results = sp.search(q=query, type='track', limit=10)
        tracks = results['tracks']['items']
        return [(track['name'], track['artists'][0]['name'], track['external_urls']['spotify']) for track in tracks]
    except Exception as e:
        print(f"Error searching Spotify: {e}")
        return []

def construct_youtube_url(query):
    return f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

def show_song_selection(songs, platform):
    def on_select_song(event):
        selected_song_index = listbox.curselection()
        if selected_song_index:
            selected_song = songs[selected_song_index[0]]
            song_name = selected_song[0]
            if platform.lower() == 'youtube':
                search_url = construct_youtube_url(song_name)
            elif platform.lower() == 'spotify':
                search_url = selected_song[2]
            else:
                messagebox.showinfo("Invalid Platform", "Please choose either 'YouTube' or 'Spotify'.")
                return
            print(f"Opening URL: {search_url}")  # Debugging line
            webbrowser.open(search_url)
            root.destroy()

    root = tk.Tk()
    root.title("Select a Song")

    tk.Label(root, text="Select a song to play:", font=('Arial', 16)).pack(pady=10)

    listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=80, height=15, font=('Arial', 12))
    for song in songs:
        listbox.insert(tk.END, f"{song[0]} - {song[1]}")
    listbox.pack(padx=10, pady=10)

    listbox.bind('<Double-1>', on_select_song)
    
    tk.Button(root, text="Cancel", command=root.quit).pack(pady=5)
    root.mainloop()

def handle_user_input(mood, language, platform, manual_query=None):
    if manual_query:
        query = manual_query
    else:
        query = spotify_queries.get(mood, {}).get(language, "")
    
    if query:
        announce(f"Searching for {query}...", language)
        songs = search_spotify(query)
        if songs:
            show_song_selection(songs, platform)
        else:
            messagebox.showinfo("No Results", "No songs found for your query.")
    else:
        messagebox.showinfo("No Query Found", "No music query found for the selected mood and language.")

def update_gif(label, gif_frames, frame_index):
    label.config(image=gif_frames[frame_index])
    frame_index = (frame_index + 1) % len(gif_frames)
    label.after(100, update_gif, label, gif_frames, frame_index)  # Update every 100ms

# Global variable to stop voice recognition
stop_recognition = False

def recognize_speech(language_code):
    global stop_recognition
    recognizer = sr.Recognizer()
    prompt_messages = {
        "en-US": "Please say a command.",
        "hi-IN": "कृपया एक आदेश कहें।",
        "te-IN": "దయచేసి ఒక ఆదేశం చెప్పండి.",
        "ta-IN": "தயவுசெய்து ஒரு கட்டளையை கூறவும்.",
        "ml-IN": "ദയവായി ഒരു ഉത്തരവാദ്യം പറയൂ."
    }
    prompt_message = prompt_messages.get(language_code, "Please say a command.")
    
    # Prompt the user
    announce(prompt_message, language_code)

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            while not stop_recognition:
                audio = recognizer.listen(source, timeout=3)  # 3-second timeout
                if language_code == "en-US":
                    query = recognizer.recognize_google(audio, language="en-US")
                elif language_code == "hi-IN":
                    query = recognizer.recognize_google(audio, language="hi-IN")
                elif language_code == "te-IN":
                    query = recognizer.recognize_google(audio, language="te-IN")
                elif language_code == "ta-IN":
                    query = recognizer.recognize_google(audio, language="ta-IN")
                elif language_code == "ml-IN":
                    query = recognizer.recognize_google(audio, language="ml-IN")
                else:
                    query = recognizer.recognize_google(audio)

                print(f"Recognized: {query}")
                return query
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return ""

def start_voice_recognition(language_code):
    global stop_recognition
    stop_recognition = False
    query = recognize_speech(language_code)
    return query

def stop_voice_recognition():
    global stop_recognition
    stop_recognition = True

def mood_language_platform_selection():
    def on_selection():
        mood = mood_var.get()
        language = language_var.get()
        platform = platform_var.get()
        manual_query = manual_search_var.get().strip()

        if manual_query:
            handle_user_input(None, None, platform, manual_query)
        elif mood and language and platform:
            announce(f"Selected mood: {mood}", language)
            announce(f"Selected language: {language}", language)
            announce(f"Selected platform: {platform}", language)
            handle_user_input(mood, language, platform)
        else:
            messagebox.showinfo("Incomplete Selection", "Please select mood, language, and platform or enter a manual search query.")

    def on_voice_command():
        language_map = {
            "English": "en-US",
            "Hindi": "hi-IN",
            "Telugu": "te-IN",
            "Tamil": "ta-IN",
            "Malayalam": "ml-IN"
        }
        selected_language = language_var.get()
        language_code = language_map.get(selected_language, "en-US")

        if selected_language:
            # Announce the prompt in the selected language
            query = start_voice_recognition(language_code)
            if query:
                # Announce the selection in all languages
                for lang in languages_list:
                    announce(f"Voice command given: {query}", lang)
                handle_user_input(None, None, platform_var.get(), manual_query=query)
            else:
                messagebox.showinfo("Voice Command Error", "Could not understand the voice command.")
        else:
            messagebox.showinfo("Language Error", "Please select a language for voice recognition.")

    root = tk.Tk()
    root.title("FEEL BEATS...")

    # Create a frame for the top section
    top_frame = tk.Frame(root, bg='lightgrey')
    top_frame.pack(fill="x", pady=10)

    # Add manual search widgets to the top frame
    manual_search_var = tk.StringVar()
    tk.Label(top_frame, text="Or enter a manual search query:", font=('Arial', 16), bg='lightgrey').pack(pady=5)
    tk.Entry(top_frame, textvariable=manual_search_var, width=50).pack(pady=5)

    # Create a canvas for background image and GIFs
    canvas = tk.Canvas(root, bg='lightgrey')
    canvas.pack(fill="both", expand=True)

    # Load and resize background image
    bg_image = Image.open("bg.png")
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Load GIFs
    gif_files = ["disco2.gif", "disco3.gif", "disco4.gif"]
    gifs = [Image.open(file) for file in gif_files]
    
    gif_frames = []
    for gif in gifs:
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
        gif_frames.extend(frames)
    
    gif_label = tk.Label(canvas)
    gif_label.pack(pady=10)
    update_gif(gif_label, gif_frames, 0)  # Start GIF update

    # Selection options for mood, language, and platform
    mood_var = tk.StringVar(value=moods_list[0])
    language_var = tk.StringVar(value=languages_list[0])
    platform_var = tk.StringVar(value="YouTube")

    tk.Label(root, text="Select Mood", font=('Arial', 16)).pack(pady=10)
    tk.OptionMenu(root, mood_var, *moods_list).pack()

    tk.Label(root, text="Select Language", font=('Arial', 16)).pack(pady=10)
    tk.OptionMenu(root, language_var, *languages_list).pack()

    tk.Label(root, text="Select Platform", font=('Arial', 16)).pack(pady=10)
    tk.OptionMenu(root, platform_var, "YouTube", "Spotify").pack()

    # Add the voice recognition and stop button
    tk.Button(root, text="Use Voice Command", command=on_voice_command).pack(pady=10)
    tk.Button(root, text="Stop Voice Recognition", command=stop_voice_recognition).pack(pady=10)

    tk.Button(root, text="Submit", command=on_selection).pack(pady=10)

    root.mainloop()

mood_language_platform_selection()
