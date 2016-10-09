import wave
import argparse
import binascii

# 128 = 0b10000000
# Therefore 128 OR'd with anything replaces the left bit to 1
MASK_ONE = 1
# 127 = 0b01111111
# Similarly 127 AND'd with anything replaces the left bit to 0
MASK_ZERO = 254

def parser():
    parser = argparse.ArgumentParser(description='Watermark your message into an audio (.wav) file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--encode', dest='encode', action='store_true', help='encodes in.wav in current directory')
    parser.add_argument('--decode', dest='decode', action='store_true', help='decodes first 5000 frames of out.wav')
    args = parser.parse_args()
    return args

def mask(data, mask_bit):
    if mask_bit == 1:
        return data | MASK_ONE
    else:
        return data & MASK_ZERO

def encode(in_wav, frames):
    odata = []
    for i in range(frames):
        frame = in_wav.readframes(1)
        iframe = bytearray(frame)
        iframe[0] = mask(iframe[0], 0)
        odata.append(bytes(iframe))
        print("Converting: {:>3.2f}%\r".format((i/frames*100)), end='')

    print("Converting: 100.00%")
    return odata

def main():
    in_wav = wave.open('in.wav', 'rb')
    depth = in_wav.getsampwidth()
    frames = in_wav.getnframes()

    print(in_wav.getparams())
    
    msg = 'Hello. This is Mitesh.'
    bmsg = [bin(ord(i)) for i in msg]
    bmsg = ''.join(bmsg).replace('0b', '')

    opts = parser()
    if opts.encode:
        out_wav = wave.open('out.wav', 'wb')
        out_wav.setparams(in_wav.getparams())
        out_data = encode(in_wav, frames)
        out_wav.writeframes(b''.join(out_data))
        print("File sucessfully written.")
        out_wav.close()
    elif opts.decode:
        out_wav = wave.open('out.wav', 'rb')
        print("Getting the LSB bits of first 5000 frames")
        for i in range(5000):
            frame = out_wav.readframes(1)
            iframe = bytearray(frame)
            print(iframe[0] & 1, end='')
        out_wav.close()
    else:
        print('Incorrect options.')
    in_wav.close()

if __name__ == '__main__':
    main()
