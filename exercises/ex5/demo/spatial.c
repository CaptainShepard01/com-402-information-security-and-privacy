#include <stdio.h>

int main() {
    int index;
    int array[] = {1, 2, 3, 4, 5, 6};

    printf("input array index: ");
    scanf("%d", &index);
    printf("array[%d] = %d\n", index, array[index]);

    return 0;
}
