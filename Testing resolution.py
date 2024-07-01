from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip

input_video_path = 'documents/private coding/twitch clips/sorted_clips/zarbex/zarbex_22.mp4'
output_video_path = 'documents/private coding/twitch clips/sorted_clips/zarbex/zarbex_22_tiktok.mp4'

def resize_with_black_bars(input_file, output_file, target_width=1080, target_height=1920):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Get the original dimensions and duration
    original_width, original_height = clip.size
    original_duration = clip.duration

    # Calculate the new dimensions while maintaining the aspect ratio
    aspect_ratio = original_width / original_height
    new_height = target_height
    new_width = int(new_height * aspect_ratio)

    # Resize the clip
    resized_clip = clip.resize(newsize=(new_width, new_height))

    # Create a black background clip with the same duration as the original clip
    black_background = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=original_duration)

    # Combine the resized clip and the black background
    final_clip = CompositeVideoClip([
        black_background,
        resized_clip.set_position(("center", "center"))
    ], size=(target_width, target_height))

    # Write the final clip to a new file
    final_clip.write_videofile(output_file)

# Example usage
resize_with_black_bars(input_video_path, output_video_path)