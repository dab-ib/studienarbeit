import asyncio
import time
import numpy as np
import av
import cv2

def motion_density_estimation(frames):
    motion_frames = 0
    total_pixels = 0
    threshold = 30

    for frame in frames:
        img_frame = frame.to_rgb().to_ndarray()
        gray_frame = cv2.cvtColor(img_frame, cv2.COLOR_RGB2GRAY)

        # Berechne die Bewegungsdifferenz zwischen dem aktuellen Frame und dem vorherigen Frame
        if motion_density_estimation.previous_frame is not None:
            frame_diff = cv2.absdiff(gray_frame, motion_density_estimation.previous_frame)
            motion_pixels = np.sum(frame_diff > threshold)  # Anzahl der bewegten Pixel über einem Schwellenwert
            motion_frames += 1 if motion_pixels > 0 else 0

        motion_density_estimation.previous_frame = gray_frame
        total_pixels += gray_frame.size

    motion_density = motion_frames / len(frames)
    density_percentage = (motion_density * 100).round(2)
    return density_percentage

motion_density_estimation.previous_frame = None

async def run():
    frame.color_range = av.ColorRange.FULL

    container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)

    frames = []
    for packet in container.demux(in_stream):
        for frame in packet.decode():
            frames.append(frame)

            # Motion Detection
            if motion_detection(frame):
                motion_density = motion_density_estimation(frames)
                print(f"Motion Density: {motion_density}%")

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
