#include <stdio.h>
#include <stdlib.h>
#include <sndfile.h>

int main(int argc, char** argv)
{
    SNDFILE *sf;
    SF_INFO info;
    int num_channels;
    int num, num_items;
    char *buf;
    int f,sr,c;
    int i,j;
    FILE *out;
    int msg_bits = 0;
    msg_bits = 5000;
    info.format = 0;
    sf = sf_open("out.wav",SFM_READ,&info);

    // save data frmo info
    f = info.frames;
    sr = info.samplerate;
    c = info.channels;
    /* printf("frames=%d\n",f); */
    /* printf("samplerate=%d\n",sr); */
    /* printf("channels=%d\n",c); */
    num_items = f*c;
    /* printf("num_items=%d\n",num_items); */
    buf = (char *) malloc(num_items*sizeof(char));
    // assume 8 bit depth
    num = sf_read_raw(sf,buf,num_items*8);
    sf_close(sf);
    printf("Read %d items\n",num);
    out = fopen("filedata.out","w");
    char hidden_msg[5000];
    int h = 0;
    int decoded_msg = 0;
    int decoded_bit = 0;
    for (i = 0; i < msg_bits; i += 1)
    {
        fprintf(out,"%d ", buf[i] & 1);
        if(i % 8 == 7){
            fprintf(out, "\n");
        }
        /* printf("%d", buf[i] & 1); */
        if(i > 63){
            if(i % 8 == 0){
                printf("%c", decoded_msg);
                decoded_msg = 0;
                decoded_bit = 0;
            }
            hidden_msg[h++] = (int)(buf[i]&1);
            decoded_bit = (int)(buf[i]&1);
            decoded_bit <<= 7-i%8;
            decoded_msg += decoded_bit;
            /* printf("%d\n", decoded_msg); */
        }
        /* printf("%d", hidden_msg[h-1]); */
    }
    fclose(out);
    return 0;
}

