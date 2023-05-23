import asyncio
import av
import cv2

async def motion_detection(frame):
    # Konvertiere das Video-Frame in ein Graustufenbild
    gray_frame = frame.to_rgb().to_gray()

    # Führe die Hintergrundsubtraktion durch
    fg_mask = motion_detection.backSub.apply(gray_frame)

    # Definiere einen Schwellenwert, um die Bewegungsmaske zu binarisieren
    threshold = 128

    # Binarisiere die Bewegungsmaske
    _, binary_mask = cv2.threshold(fg_mask, threshold, 255, cv2.THRESH_BINARY)

    # Berechne die Anzahl der weißen Pixel in der Bewegungsmaske
    motion_pixels = cv2.countNonZero(binary_mask)

    # Definiere einen Schwellenwert für die Anzahl der Bewegungspixel
    motion_threshold = 1000

    # Wenn die Anzahl der Bewegungspixel den Schwellenwert überschreitet, wird eine Bewegung erkannt
    if motion_pixels > motion_threshold:
        return True

    return False

motion_detection.backSub = cv2.createBackgroundSubtractorMOG2()

async def run():
    container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)

    for packet in container.demux(in_stream):
        for frame in packet.decode():
            # Motion Detection
            if await motion_detection(frame):

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

if __name__ == "__main__":
    asyncio.run(run())
