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
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get OAuth token: {response.json()}")
    





def get_user_id(username, oauth_token, client_id):
    url = 'https://api.twitch.tv/helix/users'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {oauth_token}'
    }
    params = {
        'login': username
    }
    response = pip._vendor.requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get user information: {response.json()}")
    



try:
    # Get OAuth token
    oauth_token = get_oauth_token(client_id, client_secret)
    print(f"OAuth Token: {oauth_token}")

    # Fetch user information
    username = ['Papaplatte', "Zarbex", "BastiGHG", "Filow", "Nooreax", "Reeze", "Trymacs", "LetsHugoTV"]
                


    for username in username:
        user_info = get_user_id(username, oauth_token, client_id)
        if user_info['data']:
            user_id = user_info['data'][0]['id']
            print(f"{username} = {user_id}")

        else:
            print(f"No user found with username: {username}")

except Exception as e:
    print(e)




