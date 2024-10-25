#include <stdio.h>
#include <pthread.h>

int counter = 0;

void *increment_counter(void *arg) {
    for (int i = 0; i < 100000; i++) {
        counter++;
        printf("thread %d: %d\n", (int) arg, counter);
    }

    return NULL;
}

int main() {
    pthread_t t[8];

    for (int tid = 0; tid < 8; tid++) {
        pthread_create(&t[tid], NULL, increment_counter, (void *) tid);
    }

    for (int tid = 0; tid < 8; tid++) {
        pthread_join(t[tid], NULL);
    }

    printf("counter = %d\n", counter);

    return 0;
}
