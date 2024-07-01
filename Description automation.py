import os
import datetime


start_path = 'documents/private coding/twitch clips/final_clips'



list_folder = [f for f in os.listdir(start_path) if not f.startswith('.') and f.endswith('.mp4')]

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

        # Format the date with periods instead of hyphens
formatted_yesterday = yesterday.strftime("%d.%m.%Y")

for index, clip in enumerate(list_folder):
        # Extract the streamer's name from the filename
        splitted_name = clip.rsplit('_', 1)
        if len(splitted_name) == 2:
            streamer_name = splitted_name[0]
        description = f'Top 3 Twitch Clips von {streamer_name} vom {formatted_yesterday} '
        hashtags = f'#{streamer_name} fyp #streamer #clips #streamerclips #twitch #deutschland'

        print (description)
        print (hashtags)

