from moviepy.editor import *
import os
import datetime

start_path = 'documents/private coding/twitch clips/sorted_clips'
final_path = 'documents/private coding/twitch clips/final_clips'

def merge_videos(start_path, final_path):
    list_folder = [f for f in os.listdir(start_path) if not f.startswith('.')]

    for folder in list_folder:
        list_subfolder = [f for f in os.listdir(f'{start_path}/{folder}') if not f.startswith(".")]

        clips = []

        for file_ in list_subfolder:
            clips.append(file_)

        final_clips = []

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        # Format the date with periods instead of hyphens
        formatted_yesterday = yesterday.strftime("%d.%m.%Y")

        i = 3

        for clip_file in (clips):
            # Load the video clip
            video_clip = VideoFileClip(f"{start_path}/{folder}/{clip_file}")

            if i == 3:
                overlay_text = f"Top 3 {folder} Clips \n vom {formatted_yesterday}\n Platz {i} "
            else:
                overlay_text = f"Platz: {i}"

            # Create the text clip with padding
            text_clip = TextClip(
                overlay_text, font="Arial-Bold", fontsize=70, color='black',
                bg_color="white", method='caption', size=(video_clip.w - 500, video_clip.h - 1500),
                align='center')

            text_clip = text_clip.set_duration(3).set_position('center')

            # Create a semi-transparent background with padding
            padding_w = 50
            padding_h = 100
            text_bg = ColorClip(
                size=(text_clip.size[0] + padding_w, text_clip.size[1] + padding_h),
                color=(255, 255, 255)).set_duration(3).set_position('center')

            # Composite the text on the background with padding
            text_bg_clip = CompositeVideoClip([text_bg.set_position('center'), text_clip.set_position('center')])

            # Composite the text background clip on the video clip
            final_clip = CompositeVideoClip([video_clip, text_bg_clip.set_position('center')])

            final_clips.append(final_clip)

            i -= 1

        # Concatenate all final clips
        if final_clips:
            merged_clip = concatenate_videoclips(final_clips)
            merged_clip.write_videofile(f"{final_path}/{folder}_merged.mp4", codec='libx264')

        # Remove original files
        for file_delete in list_subfolder:
            os.remove(f"{start_path}/{folder}/{file_delete}")


merge_videos(start_path, final_path)
