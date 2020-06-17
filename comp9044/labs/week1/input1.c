// Written by andrewt@cse.unsw.edu.au
// as a COMP2041 lecture example
// Over-simple /usr/bin/grep emulation.
// July 2015

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// print lines containing the specified substring
// breaks on long lines, does not implement regexs or other grep features
void process_stream(FILE *stream, char *stream_name, char *substring) {
    char line[65536];
    int line_number = 1;
    while (fgets(line, sizeof line, stream) != NULL) {
        if (strstr(line, substring) != NULL)
            printf("%s:%d:%s", stream_name, line_number, line);
        line_number = line_number + 1;
    }
}

// process files given as arguments
// if no arguments process stdin
int main(int argc, char *argv[]) {
    if (argc == 2)
        process_stream(stdin, "<stdin>", argv[1]);
    else
        for (int i = 2; i < argc; i++) {
            FILE *in = fopen(argv[i], "r");
            if (in == NULL) {
                fprintf(stderr, "%s: %s: ", argv[0], argv[i]);
                perror("");
                return 1;
            }
            process_stream(in, argv[i], argv[1]);
            fclose(in);
        }
    return 0;
}
