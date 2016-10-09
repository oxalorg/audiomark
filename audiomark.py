import wave
import struct
import binascii


def main():
    in_wav = wave.open('in.wav', 'rb')
    out_wav = wave.open('out.wav', 'wb')

    out_wav.setparams(in_wav.getparams())
    depth = in_wav.getsampwidth()
    frames = in_wav.getnframes()

    print(in_wav.getparams())

    message = 'Hello. This is Mitesh.'
    message = [ int(hex(ord(i)), 16) for i in message]
    

    for i in range(1000):
        frame = in_wav.readframes(1)
        Display
        print(list(bytearray(frame)), end='\t')
        if i % 6 == 0:
            print('')

if __name__ == '__main__':
    main()
