#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

// argv[1] path to image

int main(int argc,char** argv)
{
	Mat img = imread(argv[1]);
	string str = argv[1];
	string fn = ".png";
	fn = str + fn;
	cout << "Convert: " << str << " -> " << fn << endl;
	imwrite(fn, img);
	return 0;
}
