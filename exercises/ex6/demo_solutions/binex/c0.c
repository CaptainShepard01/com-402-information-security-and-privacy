#include <stdio.h>
#include <stdlib.h>

void win(){
	puts("you won!");
	system("/bin/sh");
}

int main(){
	char ov[0x10];
	int is_admin = 0;
	puts("overflow me:");
	gets(ov); 
	puts("returning now");
	if(is_admin){
		win();
	} else {
		puts("you're not admin sorry :'(");
	}
}
