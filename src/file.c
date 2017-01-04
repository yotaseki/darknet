#include <stdio.h>
#include "file.h"

FILE *fpfp;
void ffopen(char *fn)
{
	fpfp = fopen(fn,"w");
}

void ffclose()
{
	fclose(fpfp);
}

void ffprintf(char *line)
{
	fprintf(fpfp,"%s",line);
}
