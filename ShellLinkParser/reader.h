#ifndef	READER_H
#define	READER_H

#include "typedefs.h"

uint read_uint(FILE* fp);
word read_word(FILE* fp);
byte read_byte(FILE* fp);
void read_bytes(FILE* fp, byte* buff, int size);
int read_asciz(FILE* fp, byte* buff, int max_size);
int read_unicode(FILE* fp, byte* buff, int buff_size, int count);
int read_utf8(FILE* fp, byte* buff, int buff_size, int count);

#endif	// READER_H
