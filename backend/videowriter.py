import av
from typing import List
from fractions import Fraction

class VideoWriter:
    def __init__(self, file) -> None:
        self.file = file

    def open(self):
        self.__output: av.OutputContainer = av.open(self.file, 'w')

    def write_packet(self, packet: av.Packet) -> None:
        if packet is None:
            return

        res = self.__try_add_stream(packet)
        if not res:
            return

        self.__mux_one(packet)

    def write_packets(self, packets: List[av.Packet]) -> None:
        print('write_packets',packets)
        if len(packets) == 0:
            return

        res = self.__try_add_stream(packets[-1])

        # print(res,'28',packets)
        if not res:
            return
        self.__mux(packets)

            

    def close(self):
        print('closes')
        self.__output.close()

    def __try_add_stream(self, sample_packet: av.Packet) -> bool:
        print(self.__output.streams.video,'self.__output.streams')
        if len(self.__output.streams.video) == 0:
            if sample_packet.stream_index == 1: 
                self.__output.add_stream('aac',Fraction(30000,1001))

            sample_frames = sample_packet.decode()
            if len(sample_frames) == 0:
                return False

            sample_frame = [x for x in sample_frames if isinstance(x, av.VideoFrame)][0]
            self.__stream = self.__output.add_stream('libx264',Fraction(30000,1001))
    
            self.__stream.pix_fmt = sample_frame.format.name
            self.__stream.width = sample_frame.width
            self.__stream.height = sample_frame.height
            # print(self.__stream,53)
            return True
        return True

    def __mux(self, packets: List[av.Packet]):
        if len(packets) == 0:
            return

        print(type(packets),'611111111111111',packets[1])
        try:
             

            self.__output.mux(packets)
   
        
            # self.__output.close()
            
        except Exception as e:
            print(e,'65')

    def __mux_one(self, packet: av.Packet):
        if packet is None:
            return

        print(packet,73)
        try:
            self.__output.mux_one(packet)
        except Exception as e:
            print(e)