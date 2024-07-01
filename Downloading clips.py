import pip._vendor.requests
import datetime
import os



client_id = '2cyoaovb86dd8jxg9em3j1qtdvsvuw'
client_secret = 'vex5oce8w2s6jt06wqwicqo5eox6jt'

def get_oauth_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = pip._vendor.requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get OAuth token: {response.json()}")
    

oauth_token = get_oauth_token(client_id, client_secret)


day_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)).replace(microsecond=0).isoformat("T")


def get_clips(broadcaster_id, oauth_token, client_id):
    url = 'https://api.twitch.tv/helix/clips'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    params = {
        'broadcaster_id': broadcaster_id,
        'first': 3,  
        'started_at': day_ago

    }
    response = pip._vendor.requests.get(url, headers=headers, params=params)
    return response.json()

broadcaster_id = ['50985620',  #Papaplatte
                  '403594122', #Zarbex
                  '38121996',  #BastiGHG
                  '107888182', #Filow
                  '172312401', #Nooreax
                  '80474667'   #Reeze
                  '64342766',   #Trymacs
                  '117385099',  #LetsHugoTV

]



def prepare_and_download_clip(clips, download_folder= 'documents/private coding/twitch clips/clips'):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    for clip in clips['data']:
        clip_url = clip['thumbnail_url'].split('-preview-')[0] + '.mp4'
        streamer_name = clip['broadcaster_name']
        clip_title = clip['title'].replace(' ', '_').replace('/', '_')
        download_path = os.path.join(download_folder, f"{clip_title}_{streamer_name}.mp4") 
        download_clip(clip_url, download_path)
        print(f"Downloaded: {clip_title}")

    

def download_clip(clip_url, download_path):
    
    response = pip._vendor.requests.get(clip_url, stream=True)
    if response.status_code == 200:
        with open(download_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)


for current_streamer in broadcaster_id:

    clips = get_clips(current_streamer, oauth_token, client_id)
    #created_at = clips['data'][0]['created_at']
    prepare_and_download_clip(clips)