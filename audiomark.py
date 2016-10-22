import sys
import wave
import argparse
import binascii

# OR'ing anything with 0b01 replaces LSB to 1
MASK_ONE = 1
# Similarly AND'ing anything with 0b11111110 replaces the LSB to 0
MASK_ZERO = 254

def parser():
    parser = argparse.ArgumentParser(description='Watermark your message into an audio (.wav) file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--encode', dest='encode', action='store_true', help='encodes in.wav in current directory')
    parser.add_argument('--decode', dest='decode', action='store_true', help='decodes first 5000 frames of out.wav')
    parser.add_argument('--message', dest='msg')
    args = parser.parse_args()
    return args

def mask(data, mask_bit):
    '''
    Replaces the LSB of `data` with `mask_bit`
    '''
    if mask_bit == 1:
        return data | MASK_ONE
    else:
        return data & MASK_ZERO

def encode(in_wav, frames, msg_bit):
    '''
    overwrite the least significant bit of the frame
    by masking it with a single bit from the message
    '''
    odata = []
    for i in range(frames):
        frame = in_wav.readframes(1)
        iframe = bytearray(frame)
        iframe[0] = mask(iframe[0], next(msg_bit))
        odata.append(bytes(iframe))
        print("Converting: {:>3.2f}%\r".format((i/frames*100)), end='')

    print("Converting: 100.00%")
    return odata


def msg_bit_gen(msg):
    '''
    takes input message and returns a binary generator/iterator
    first 64 bits returned are the message length
    '''
    bmsg = ''.join([ '{:016b}'.format(ord(i)) for i in msg])
    bmsg_size = '{:064b}'.format(len(bmsg)) # 64 bit binary representation
    print('Message in binary: ' + bmsg)
    for bit in bmsg_size:
        yield int(bit)
    for bit in bmsg:
        yield int(bit)
    while True:
        yield 0

def main():
    in_wav = wave.open('in.wav', 'rb')
    depth = in_wav.getsampwidth()
    frames = in_wav.getnframes()

    print(in_wav.getparams())

    opts = parser()
    msg_bit = msg_bit_gen(opts.msg)

    if opts.encode:
        out_wav = wave.open('out.wav', 'wb')
        out_wav.setparams(in_wav.getparams())
        out_data = encode(in_wav, frames, msg_bit)
        out_wav.writeframes(b''.join(out_data))
        print("File sucessfully written.")
        out_wav.close()
    elif opts.decode:
        out_wav = wave.open('out.wav', 'rb')
        size = frames
        size_string = ''
        msg_string = ''
        i = 0
        while size:
            frame = out_wav.readframes(1)
            iframe = bytearray(frame)
            print(iframe)
            # print(iframe[0] & 1, end='')
            if i < 64:
                # first 64 bits are message length
                size_string += '' + str(iframe[0] & 1)
                i += 1
            elif i == 64:
                size = int(size_string, 2)
                print('\nSize of watermarked msg: ' + str(size) + ' bits.')
                i += 1
            else:
                # rest of the bits are the actual message
                msg_string += str(iframe[0] & 1)
                size -= 1

        print('Hidden message in binary: ' + msg_string)
        msg_decoded = [ chr(int(msg_string[i:i+7], 2)) for i in range(0, len(msg_string), 8)]
        print('\n The message decoded is: ' + ''.join(msg_decoded))
        out_wav.close()
    else:
        print('Incorrect options.')
    in_wav.close()


if __name__ == '__main__':
    main()

# TODO
# ----
# Don't read frames one at a time. Read everything together
# and then do the encoding using bit depth and channel size.
#
