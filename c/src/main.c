#include <time.h> 
#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include "EPD_5in83_V2.h"
#include "DEV_Config.h"
#include "GUI_Paint.h"
#include "GUI_BMPfile.h"
#include "Debug.h"

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:exit\r\n");
    DEV_Module_Exit();
    exit(0);
}

int draw_bit_map(int i);

int main(void)
{
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    // drawing bitmap with index i
    int ret = draw_bit_map(1);
    
    // Check the return value for errors
    if (ret == -1) {
        printf("Error occurred during drawing.\n");
    }

    return 0;
}


int draw_bit_map(int i) {
    printf("Drawing quote from bitmap\r\n");
    if(DEV_Module_Init()!=0){
        return -1;
    }

    // clear e-paper and init memory 
    printf("e-Paper Init and Clear...\r\n");
    EPD_5in83_V2_Init();
	struct timespec start={0,0}, finish={0,0}; 
    clock_gettime(CLOCK_REALTIME,&start);
    EPD_5in83_V2_Clear();
	clock_gettime(CLOCK_REALTIME,&finish);
    printf("%ld S\r\n",finish.tv_sec-start.tv_sec);
	
    DEV_Delay_ms(500);

    // create a new image cache named IMAGE_BW and fill it with white
    UBYTE *BitMapImage;
    UWORD Imagesize = ((EPD_5in83_V2_WIDTH % 8 == 0)? (EPD_5in83_V2_WIDTH / 8 ): (EPD_5in83_V2_WIDTH / 8 + 1)) * EPD_5in83_V2_HEIGHT;
    if((BitMapImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        return -1;
    }

    printf("NewImage: BitMapImage\r\n");
    Paint_NewImage(BitMapImage, EPD_5in83_V2_WIDTH, EPD_5in83_V2_HEIGHT, 180, WHITE);

    // load and draw bmp
    printf("load bmp\r\n");
    Paint_SelectImage(BitMapImage);
    GUI_ReadBmp("/home/justus/quotes/bmp/2.bmp", 0, 0);
    printf("drawing...\r\n");
    EPD_5in83_V2_Display(BitMapImage);
    DEV_Delay_ms(2000);

    printf("go to Sleep...\r\n");
    EPD_5in83_V2_Sleep();
    free(BitMapImage);
    BitMapImage = NULL;
    DEV_Delay_ms(2000);//important, at least 2s
    // close 5V
    printf("close 5V, Module enters 0 power consumption ...\r\n");
    DEV_Module_Exit();
    
    return 0;
}
