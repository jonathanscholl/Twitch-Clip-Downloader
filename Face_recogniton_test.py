import cv2
import face_recognition
import numpy as np

# Paths to the input and output videos
input_video_path = 'documents/private coding/twitch clips/sorted_clips/zarbex/zarbex.mp4'
output_video_path = 'documents/private coding/twitch clips/sorted_clips/zarbex/zarbex_22_tiktok.mp4'

# Open the input video
cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec and create a VideoWriter object for the output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (1080, 1920))

# Read the first frame to get the facecam region
ret, frame = cap.read()
if not ret:
    print("Failed to read the video")
    cap.release()
    exit()

# Define the region of interest (top-left part of the frame)
roi_width = frame.shape[1]  # Adjust as needed
roi_height = frame.shape[0] // 4  # Adjust as needed


roi = frame[:roi_height, :]

# Convert the ROI to RGB for face detection
rgb_roi = roi[:, :, ::-1]

# Detect the face in the ROI
face_locations = face_recognition.face_locations(rgb_roi)
if face_locations:
    top, right, bottom, left = face_locations[0]
    facecam_region = (left, top, right, bottom)
else:
    print("No facecam found")
    cap.release()
    out.release()
    exit()


expand_percentage_height = 1
expand_percentage_width = 10 

# Calculate the facecam region in the original frame
left, top, right, bottom = facecam_region
facecam_width = right - left
facecam_height = bottom - top

expand_width = int(facecam_width * expand_percentage_width)
expand_height = int(facecam_height * expand_percentage_height)

new_left = max(0, left - expand_width)
new_top = max(0, top - expand_height)
new_right = min(frame.shape[1], right + expand_width)
new_bottom = min(frame.shape[0], bottom + expand_height)


facecam_region = (new_left, new_top, new_right, new_bottom)


# Re-open the input video for processing
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the first frame

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Extract the facecam region from the frame
    facecam = frame[new_top:new_bottom, new_left:right]

    # Resize the facecam to fit the top 1/4 of the 9:16 frame (1080x480)
    target_facecam_height = 1920 // 3
    target_facecam_width = int(target_facecam_height * facecam_width / facecam_height)
    resized_facecam = cv2.resize(facecam, (target_facecam_width, target_facecam_height))

    # Center the facecam horizontally within 1080 width, pad if necessary
    padded_facecam = np.zeros((target_facecam_height, 1080, 3), dtype=np.uint8)
    pad_x = (1080 - target_facecam_width) // 2
    padded_facecam[:, pad_x:pad_x + target_facecam_width] = resized_facecam

    # Extract the game content (the rest of the frame below the facecam)
    game_content = frame[new_bottom :, right:right + 1000]

    # Resize the game content to fit the lower 3/4 of the 9:16 frame
    target_game_content_height = 1920 - target_facecam_height
    resized_game_content = cv2.resize(game_content, (1080, target_game_content_height))

    # Create the final 9:16 frame by concatenating facecam and game content vertically
    tiktok_frame = np.vstack((padded_facecam, resized_game_content))

    # Write the frame to the output video
    out.write(tiktok_frame)

# Clean up
cap.release()
out.release()

print("Video processing completed and saved to", output_video_path)
