#include <stdio.h>

void print_long(long x) {
    for (int i = 7; i >= 0; i--) {
        putchar(x >> (i * 8));
    }
}

int main() {
    long x8 = 0x4f;
    long x10 = 0x14be74f15;
    long x18 = 0x4;
    long x20 = 0x3;
    long x28 = 0x13;
    long x30 = 0x115;
    long x38 = 0x77cf4b645b61;
    long x40 = 0x2;
    long x48 = 0x11;
    long x50 = 0x21c1;
    long x58 = 0x182265e9;
    long x60 = 0x833;
    long x68 = 0xaab;
    long x70 = 0x8daaad;
    long rax = x8;
    rax *= x10;
    long x78 = rax;
    rax = x18;
    rax *= x20;
    rax *= x28;
    rax *= x30;
    rax *= x38;
    long x80 = rax;
    rax = x40;
    rax *= x48;
    rax *= x50;
    rax *= x58;
    long x88 = rax;
    rax = x60;
    rax *= x68;
    rax *= x70;
    long x90 = rax;
    print_long(x78);
    print_long(x80);
    print_long(x88);
    print_long(x90);
    return 0;
}
