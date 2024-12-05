#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    char input[50];
    printf("Enter password: ");
    scanf("%49s", input);

    if (strcmp(input, "password") == 0) {
        printf("true\n");
        return 0;
    } else {
        printf("Incorrect password.\n");
        exit(1);
    }
}
