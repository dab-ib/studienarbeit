def __capture_thread(self, cam: Camera, buffer: FrameBuffer):
    container = av.open(cam.url)
    in_stream = container.streams.video[0]
    test_output = av.open('output_vid_39.mp4', 'w')
# out_stream = test_output.add_stream(template=in_stream)  # Using template=in_stream is not working (probably meant to be used for re-muxing and not for re-encoding).
    codec_name = in_stream.codec_context.name  
    print('codec_name',codec_name)
    # Get the codec name from the input video stream.
    fps = in_stream.codec_context.rate  # Get the framerate from the input video stream.
    out_stream = test_output.add_stream(codec_name)
    out_stream.width = in_stream.codec_context.width  # Set frame width to be the same as the width of the input stream
    out_stream.height = in_stream.codec_context.height  # Set frame height to be the same as the height of the input stream
    out_stream.pix_fmt = in_stream.codec_context.pix_fmt  
    count = 0
    last_pts = 0
    for packet in container.decode():
        try:
            if not isinstance(packet.pts, int):
                continue
            img_frame = packet.to_image()
            out_frame = av.VideoFrame.from_image(img_frame)
            out_packet = out_stream.encode(out_frame)
            print(out_packet,'sssssssssssssss')
            # Encode video frame
            test_output.mux(out_packet) 
            buffer.add(out_packet)
                # "Mux" the encoded frame (add the encoded frame to MP4 file).
            if count  > 10:
                break
            count = count + 1
        except:
            pass



            
            # if not isinstance(packet.pts, int):
            #     continue
            # if packet.pts > last_pts:
            #     last_pts = packet.pts
            #     buffer.add(packet)
        test_output.close()
        # test_output.close()
        return
    #def get_player(self, id: int) -> MediaPlayer:
    #    return self.__players[id]