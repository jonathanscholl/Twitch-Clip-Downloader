import pip._vendor.requests
import datetime



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


week_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=3)).replace(microsecond=0).isoformat("T")


def get_clips(broadcaster_id, oauth_token, client_id):
    url = 'https://api.twitch.tv/helix/clips'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    params = {
        'broadcaster_id': broadcaster_id,
        'first': 3,  
        'started_at': week_ago

    }
    response = pip._vendor.requests.get(url, headers=headers, params=params)
    return response.json()

broadcaster_id = '172312401'
clips = get_clips(broadcaster_id, oauth_token, client_id)
#created_at = clips['data'][0]['created_at']
print(clips)




