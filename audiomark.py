import wave
import struct
import binascii


def main():
    in_wav = wave.open('in.wav', 'rb')
    out_wav = wave.open('out.wav', 'wb')

    out_wav.setparams(in_wav.getparams())

    frames = in_wav.getnframes()

    data = str(in_wav.readframes(100))
    # un = struct.unpack('b', data)
    for line in data.split('\n'):
        un = binascii.hexlify(line)
        print(un)
    # for frame in range(frames):
    #     print(str(in_wav.readframes(frame)))
    #     if frame > 100:
    #         return
    #     else:
    #         continue


if __name__ == '__main__':
    main()
