import cv2


def create_sliding_animation(src_image: str,
                             duration: int,
                             padding_ratio: float, # cannot be greater than 0.5 * width_reduction_ratio
                             target_video_path: str,
                             fps: int = 25,
                             width_reduction_ratio: float = 0.5625):
    source = cv2.imread(src_image)
    num_frames = duration * fps

    target_height = source.shape[0]
    target_width = int(source.shape[1] * width_reduction_ratio)

    slide_per_frame = (source.shape[1]*(1 - 2 * padding_ratio) - target_width) / num_frames
    start_width_offset = source.shape[1] * padding_ratio

    print(target_width, target_height, slide_per_frame, start_width_offset)

    # Create a video writer object
    output = cv2.VideoWriter(target_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (target_width, target_height))

    # Generate frames with sliding effect
    for i in range(num_frames):
        start_x = int(start_width_offset + (slide_per_frame * i))
        end_x = start_x + target_width

        # Crop the image to the current frame's view
        print(f"Frame: {i}: Height: 0:{target_height}, Width: {start_x}:{end_x}")
        frame = source[0:target_height, start_x:end_x]

        # Add the frame to the video
        output.write(frame)

    # Release the video writer object
    output.release()

if __name__ == "__main__":
    create_sliding_animation("vegeta.jpeg", 5, 0.1, "vegeta.mp4")

