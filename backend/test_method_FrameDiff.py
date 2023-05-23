import asyncio
import av
import numpy as np

def motion_detection(frame, prev_frame):
    # Konvertiere das Video-Frame in ein Graustufenbild
    gray_frame = frame.to_rgb().to_gray()

    # Berechne die Differenz zwischen dem aktuellen Frame und dem vorherigen Frame
    frame_diff = np.abs(gray_frame - prev_frame)

    # Definiere einen Schwellenwert, um die Pixelunterschiede zu erfassen
    threshold = 30

    # Berechne den Durchschnittswert der Pixelunterschiede im Bild
    mean_diff = np.mean(frame_diff)

    # Wenn der Durchschnittswert der Pixelunterschiede den Schwellenwert überschreitet, wird eine Bewegung erkannt
    if mean_diff > threshold:
        return True

    return False

async def run():
    container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)

    prev_frame = None

    for packet in container.demux(in_stream):
        for frame in packet.decode():
            # Motion Detection
            if prev_frame is not None and motion_detection(frame, prev_frame):
            prev_frame = frame

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

if __name__ == "__main__":
    asyncio.run(run())