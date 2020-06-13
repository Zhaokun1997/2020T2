// Written by andrewt@cse.unsw.edu.au
// as a COMP2041 lecture example
// Over-simple /usr/bin/uniq emulation.
// July 2015

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 65536

// cope stream to stdout except for repeated lines
void process_stream(FILE *stream) {
    char line[MAX_LINE];
    char lastLine[MAX_LINE];
    int line_number = 0;

    while (fgets(line, MAX_LINE, stdin) != NULL) {
        if (line_number == 0 || strcmp(line, lastLine) != 0) {
            fputs(line, stdout);
            strncpy(lastLine, line, MAX_LINE);
        }
        line_number++;
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
