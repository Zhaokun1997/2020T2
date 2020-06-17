// Written by andrewt@cse.unsw.edu.au
// as a COMP2041 lecture example
// Simple /usr/bin/wc emulation.
// July 2015

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

// count lines, words, chars in stream
void process_stream(FILE *in) {
    int n_lines = 0, n_words = 0, n_chars = 0;
    int in_word = 0, c;
    while ((c = fgetc(in)) != EOF) {
        n_chars++;
        if (c == '\n')
            n_lines++;
        if (isspace(c))
            in_word = 0;
        else if (!in_word) {
            in_word = 1;
            n_words++;
        }
    }
    printf("%6d %6d %6d", n_lines, n_words, n_chars);
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
            printf(" %s\n", argv[i]);
            fclose(in);
        }
    return 0;
}
