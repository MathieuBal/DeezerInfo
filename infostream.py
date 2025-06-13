import os
import requests
import time
import json
import webbrowser


APP_ID = os.getenv('APP_ID', '****')
APP_SECRET = os.getenv('APP_SECRET', '****')
REDIRECT_URI = 'http://localhost/dashboard/'
TOKEN_FILE = 'dist/deezer_token.txt'
DATA_FILE = 'dist/deezer_data.json'

last_track_id = None

print("Démarrage du script...")
print("Tentative d'authentification...")

# Obtenir le token d'accès
if not os.path.exists(TOKEN_FILE):
    AUTH_URL = f"https://connect.deezer.com/oauth/auth.php?app_id={APP_ID}&redirect_uri={REDIRECT_URI}&perms=basic_access,offline_access,listening_history"
    webbrowser.open(AUTH_URL)
    code = input("Entrez le code obtenu après l'authentification: ")
    response = requests.post(f"https://connect.deezer.com/oauth/access_token.php?app_id={APP_ID}&secret={APP_SECRET}&code={code}")
    access_token = response.text.split('=')[1].split('&')[0]

    with open(TOKEN_FILE, 'w') as f:
        f.write(access_token)
else:
    with open(TOKEN_FILE, 'r') as f:
        access_token = f.read()

print("Authentification réussie. Token obtenu.")
print("Tentative de récupération de la playlist 'stream'...")

# Obtenir la playlist "stream"
def get_stream_playlist(access_token):
    index = 0
    while True:
        response = requests.get(f"https://api.deezer.com/user/me/playlists?access_token={access_token}&index={index}&limit=50")
        playlists = response.json()['data']
        if not playlists:
            return None

        for playlist in playlists:
            if playlist['title'] == 'stream':
                return playlist

        index += 50
    return None

stream_playlist = get_stream_playlist(access_token)
if not stream_playlist:
    print("Playlist 'stream' non trouvée!")
    exit()

print("Playlist 'stream' récupérée avec succès.")
print("Tentative de récupération des morceaux de la playlist 'stream'...")

# Obtenir les morceaux de la playlist "stream"
def get_stream_playlist_tracks(playlist_url, access_token):
    all_tracks = []
    index = 0
    while True:
        response = requests.get(f"{playlist_url}?access_token={access_token}&index={index}&limit=50")
        if response.status_code == 200:
            tracks = response.json()['data']
            if not tracks:  
                break
            all_tracks.extend(tracks)
            index += len(tracks)  
        else:
            break
    return all_tracks


tracks = get_stream_playlist_tracks(stream_playlist['tracklist'], access_token)
if not tracks:
    print("Aucun morceau trouvé pour la playlist 'stream'.")
else:
    print(f"{len(tracks)} morceaux récupérés pour la playlist 'stream'.")

stream_playlist['tracks_data'] = tracks

print("Chargement de la playlist et des morceaux du fichier JSON...")

# Charger les données existantes
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as json_file:
        stream_playlist = json.load(json_file)
    print("le fichier JSON est bien chargé...")

else:
    stream_playlist = None

# Vérifier si la playlist doit être mise à jour
print("Vérification de la playlist...")

if stream_playlist:
    response = requests.get(f"https://api.deezer.com/playlist/{stream_playlist['id']}?access_token={access_token}")
    if response.status_code == 200 and response.json()['nb_tracks'] != len(stream_playlist.get('tracks_data', [])):
        
        # Mise à jour nécessaire
        print("Mise a jour de la playlist...")

        tracks = get_stream_playlist_tracks(stream_playlist['tracklist'], access_token)
        stream_playlist['tracks_data'] = tracks

        with open(DATA_FILE, 'w') as json_file:
            json.dump(stream_playlist, json_file)

        print("Mise a jour de la playlist réussi...")

else:
    print("Écriture de la playlist et des morceaux dans le fichier JSON...")
    stream_playlist = get_stream_playlist(access_token)
    tracks = get_stream_playlist_tracks(stream_playlist['tracklist'], access_token)
    stream_playlist['tracks_data'] = tracks

    with open(DATA_FILE, 'w') as json_file:
        json.dump(stream_playlist, json_file)
    print("Les données ont été écrites avec succès dans le fichier JSON.")

# Comparer l'historique de lecture avec la playlist
while True:
    print("Récupération de l'historique de lecture...")

    history_track_id = requests.get(f"https://api.deezer.com/user/me/history?access_token={access_token}").json()['data'][0]['id']

    print(f"Dernier titre écouté ID: {history_track_id}")

    current_track = None
    for track in stream_playlist['tracks_data']:
        if track['id'] == history_track_id:
            # Récupérer l'index du morceau en cours dans la playlist
            current_index = stream_playlist['tracks_data'].index(track)
            # Prendre le morceau suivant comme morceau en cours
            current_track = stream_playlist['tracks_data'][(current_index + 1) % len(stream_playlist['tracks_data'])]
            break

    if current_track and current_track['id'] != last_track_id:
        with open('current_song.txt', 'w', encoding='utf-8') as f:
            f.write(
                f"Titre: {current_track['title']} - Artiste: {current_track['artist']['name']} - Album: {current_track['album']['title']}    ")

        last_track_id = current_track['id']

    if current_track:
        print(f"Titre en cours: {current_track['title']} - Artiste: {current_track['artist']['name']} - Album: {current_track['album']['title']}")

    time.sleep(5)
