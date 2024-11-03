#include <stdio.h>
#include <stdlib.h>

void win(){
	puts("you won!");
	system("/bin/sh");
}

int main(){
	char ov[0x10];
	puts("overflow me:");
	gets(ov); 
	puts("returning now");
}
