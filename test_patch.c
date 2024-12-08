#include <stdio.h>
#include <unistd.h>

int main() {
    printf("waiting...\n");
    sleep(5);
    printf("hello\n");
    return 0;
}
