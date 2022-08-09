/*****************************************************************************
* | File      	:   main.c
* | Author      :   Waveshare team & Prashant Nandipati
* | Function    :   Modified Epaper image display from cli
* | Info        :
*----------------
* |	This version:   V1.0.1
* | Date        :   2022-08-2
* | Info        :
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
******************************************************************************/
#include "EPD_7in5b_V2.h"
#include <time.h> 
#include <stdlib.h>

#define _EPD_TEST_H_

#include "DEV_Config.h"
#include "GUI_Paint.h"
#include "GUI_BMPfile.h"
#include "ImageData.h"

UBYTE *BlackImage, *RYImage;
UWORD Imagesize;

void setup_img_buffers(){
    Imagesize = ((EPD_7IN5B_V2_WIDTH % 8 == 0)? (EPD_7IN5B_V2_WIDTH / 8 ): (EPD_7IN5B_V2_WIDTH / 8 + 1)) * EPD_7IN5B_V2_HEIGHT;
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        return -1;
    }
    if((RYImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for red memory...\r\n");
        return -1;
    }
    Paint_NewImage(BlackImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
    Paint_NewImage(RYImage, EPD_7IN5B_V2_WIDTH, EPD_7IN5B_V2_HEIGHT , 0, WHITE);
}


int main(int argc,char* argv[]){
    if(argc < 2) printf("./epd blackimage.bmp redimage.bmp\n");
    setbuf(stdout, NULL);
    if(DEV_Module_Init()!=0) return -1;
    EPD_7IN5B_V2_Init();
    setup_img_buffers();
    Paint_SelectImage(BlackImage);
    GUI_ReadBmp(argv[1], 0, 0);
    Paint_SelectImage(RYImage);
    GUI_ReadBmp(argv[2], 0, 0);
    EPD_7IN5B_V2_Display(BlackImage, RYImage);
    DEV_Delay_ms(100);

    return 0;
}

