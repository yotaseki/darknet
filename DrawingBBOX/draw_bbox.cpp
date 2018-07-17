#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>
using namespace std;
using namespace cv;
/*
 * [1] predict
 * [2] teacher
 * [3] image
 * [4] class
 * [5] 0 or 1 or 2 (both / teacher_only / predict_only)
 * [6] output
 */

int main (int argc,char **argv)
{
    int cls = 0;
	if(argc != 6)
    {
        printf("invalid argument ;%d\n",argc);
		return -1;
    }
	Mat im = imread(argv[3]);
    if(im.empty())
    {
        cout <<"input error: " << argv[3] << endl;
        return -1;
    }
	string str;
	char fn[256];
	FILE *pfp,*tfp;
	int ret;
	int c,px,py,Px,Py;
	int tx,ty,Tx,Ty;
    int sw = atoi(argv[4]);
    int ac;
	if((pfp = fopen(argv[1],"r"))==NULL){
		printf("arg[1]:Annotation.txt open error\n");
		printf("%s\n",argv[1]);
		exit(EXIT_FAILURE);
	}
	if((tfp = fopen(argv[2],"r"))==NULL){
		printf("arg[2]:Annotation.txt open error\n");
		printf("%s\n",argv[2]);
		exit(EXIT_FAILURE);
	}
	while(( ret = fscanf( tfp , "%d%d%d%d%d",&c,&tx,&ty,&Tx,&Ty )) != EOF ) {
		if(tx > -1 && c==cls)
			if(sw == 1)
            {
				rectangle(im,Rect(tx,ty,Tx-tx,Ty-ty),Scalar(0,255,255),3);
            }
		continue;
	}
	while(( ret = fscanf( pfp , "%d%d%d%d%d%d",&c,&px,&py,&Px,&Py,&ac )) != EOF ) {
		if(px > -1 && c==cls)
			if(sw == 2)
            {
				rectangle(im,Rect(px,py,Px-px,Py-py),Scalar(0,0,255),3);
            }
		if(px > -1 && c!=cls)
			if(sw == 2)
            {
				rectangle(im,Rect(px,py,Px-px,Py-py),Scalar(0,255,0),3);
            }
		continue;
	}
	sprintf(fn,"%s_test.jpg",argv[5]);
	str = fn;
    printf("%s\n",fn);
	imwrite(str,im);
	fclose(tfp);
	fclose(pfp);

	return 0;

}
