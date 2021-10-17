#include <stdlib.h>
#include <stdio.h>

void main(int t) {
	//Loop infinito
	for(t=0;;++t) 
		putchar(t*((t>>12|t>>8) & 63 & t >> 4));
}
