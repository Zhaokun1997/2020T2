// Written by andrewt@cse.unsw.edu.au
// as a COMP2041 lecture example
// July 2015
// Simple /bin/cat emulation.

#include <stdio.h>
#include <stdlib.h>

// write bytes of stream to stdout
void process_stream(FILE *in) {
    while (1) {
        int ch = fgetc(in);
        if (ch == EOF)
             break;
        if (fputc(ch, stdout) == EOF) {
            fprintf(stderr, "cat:");
            perror("");
            exit(1);
        }
    }
}

// process files given as arguments
// if no arguments process stdin
int main(int argc, char *argv[]) {
    if (argc == 1)
        process_stream(stdin);
    else
        for (int i = 1; i < argc; i++) {
            FILE *in = fopen(argv[i], "r");
            if (in == NULL) {
                fprintf(stderr, "%s: %s: ", argv[0], argv[i]);
                perror("");
                return 1;
            }
            process_stream(in);
            fclose(in);
        }
    return 0;
}
