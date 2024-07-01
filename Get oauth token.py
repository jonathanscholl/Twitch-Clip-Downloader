import pip._vendor.requests

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
    return response.json()['access_token']

oauth_token = get_oauth_token(client_id, client_secret)
print(oauth_token)
