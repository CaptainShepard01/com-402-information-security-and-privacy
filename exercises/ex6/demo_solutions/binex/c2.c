#include <stdio.h>
#include <stdlib.h>

char* IGNORE_ME = "/bin/sh";

// this is dead code TODO: remove
void why(){
	long value = 42;
	long value2;
asm volatile (
        "push %0;"     
        "pop %%rdi;"   
	"ret;"
	: "=r" (value2)  
	: "r" (value)  
        : "%rdi"       
    );
}

void win(){
	puts("do it yourself!");
	system("echo \"no code exec for you..\"");
}

int main(){
	char ov[0x10];
	puts("overflow me:");
	gets(ov); 
	puts("returning now");
}
