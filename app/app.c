#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "h_files/engine.h"

static int parse_line(const char* line, int* iteration, int* ignition) {
    // Expect: iteration,ignition_switch
    // Skip header if present
    if (strstr(line, "iteration") && strstr(line, "ignition_switch")) return 1;
    int it = 0, ign = 0;
    if (sscanf(line, " %d , %d ", &it, &ign) == 2) {
        *iteration = it; *ignition = ign; return 0;
    }
    return -1;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <input_csv> <output_csv>\n", argv[0]);
        return 2;
    }

    const char* in_path  = argv[1];
    const char* out_path = argv[2];

    FILE* fin = fopen(in_path, "r");
    if (!fin) {
        perror("open input");
        return 3;
    }
    FILE* fout = fopen(out_path, "w");
    if (!fout) {
        perror("open output");
        fclose(fin);
        return 4;
    }

    engine_init();

    // Write header for output
    fprintf(fout, "iteration,ignition_switch,engine_state\n");

    char buf[512];
    while (fgets(buf, sizeof(buf), fin)) {
        // skip empty lines
        if (buf[0] == '\n' || buf[0] == '\r' || buf[0] == '\0') continue;

        int it = 0, ign = 0;
        int r = parse_line(buf, &it, &ign);
        if (r == 1) continue;          // it was a header
        if (r == -1) continue;         // malformed line; skip silently

        engine_update((uint8_t)ign);
        fprintf(fout, "%d,%d,%d\n", it, ign, (int)engine_state);
    }

    fclose(fin);
    fclose(fout);
    return 0;
}
