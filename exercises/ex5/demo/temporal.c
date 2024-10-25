#include <stdio.h>
#include <stdlib.h>

int main() {
    int *ptr =  malloc(sizeof(int));

    *ptr = 1;

    printf("*ptr = %d\n", *ptr);

    free(ptr);

    printf("ptr freed\n");

    printf("try to access ptr again, *ptr = %d\n", *ptr);

    return 0;
}
