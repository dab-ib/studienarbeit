import asyncio
import av
import numpy as np

async def motion_detection(frame):
    # Konvertiere das Video-Frame in ein Graustufenbild
    gray_frame = frame.to_rgb().to_gray()

    # Berechne die Differenz zwischen dem aktuellen Frame und dem vorherigen Frame
    if motion_detection.previous_frame is None:
        motion_detection.previous_frame = gray_frame
        return False

    frame_diff = np.abs(gray_frame - motion_detection.previous_frame)
    motion_detection.previous_frame = gray_frame

    # Definiere einen Schwellenwert, um die Helligkeitsänderung zu erfassen
    threshold = 70

    # Berechne den Durchschnittswert der Helligkeitsänderung im Bild
    mean_diff = np.mean(frame_diff)

    # Wenn die durchschnittliche Helligkeitsänderung den Schwellenwert überschreitet, wird eine Bewegung erkannt
    if mean_diff > threshold:
        print("Bewegung erkannt!")
        return True

    return False

motion_detection.previous_frame = None

async def run():
    container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)

    for packet in container.demux(in_stream):
        for frame in packet.decode():
            # Motion Detection
            if await motion_detection(frame):
                pass

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

if __name__ == "__main__":
    asyncio.run(run())
