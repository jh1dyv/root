 // reader.cpp
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <locale.h>
#include "typedefs.h"
extern const char* prog;
extern long fpos;

uint read_uint(FILE* fp) {
	uint buff;
	if (fread(&buff, sizeof(uint), 1, fp) != 1) {
		fprintf(stderr, "%s: read error: read_uint (%d)\n", prog, ferror(fp));
	}
	fpos += sizeof(uint);
	return buff;
}

word read_word(FILE* fp) {
	word buff;
	if (fread(&buff, sizeof(word), 1, fp) != 1) {
		fprintf(stderr, "%s: read error: read_word (%d)\n", prog, ferror(fp));
	}
	fpos += sizeof(word);
	return buff;
}

byte read_byte(FILE* fp) {
	byte buff;
	if (fread(&buff, sizeof(byte), 1, fp) != 1) {
		if (feof(fp)) {
			fprintf(stderr, "%s: premature eof\n", prog);
		} else {
			fprintf(stderr, "%s: read error: read_byte (errno %d)\n",
				prog, ferror(fp));
		}
	}
	fpos += sizeof(byte);
	return buff;
}

void read_bytes(FILE* fp, byte* buff, int size) {
	for (int n = 0; n < size; n++) {
		buff[n] = read_byte(fp);
	}	
}

int read_asciz(FILE* fp, byte* buff, int buff_size) {
	byte* cp = buff;
	int size = 0;
	while (++size < buff_size) {
		*cp++ = read_byte(fp);
		if (*(cp-1) == '\0')
			break;
	}
	*cp = '\0';
	return size;
}

#define	botch(msg) fprintf(stderr, "Botch: %s\n", msg)
static size_t count_sjis_bytes(wchar_t[], int);

int read_unicode(FILE* fp, byte* buff, int buff_size, int count) {
	wchar_t w_buff[1024];
	int in_bytes = (int) (sizeof(wchar_t) * count);
	if (fread(&w_buff, sizeof(wchar_t), count, fp) != count) {
		fprintf(stderr, "%s: read error: read_byte\n", prog);
	}
	fpos += in_bytes;
	// unicodeをsjisに変換したときのバイト数を数える
	size_t sjis_bytes = count_sjis_bytes(w_buff, count);
	size_t ret;
	errno_t err = wcstombs_s(&ret,
			(char*) buff, (size_t) buff_size,
			(const wchar_t*) w_buff, sjis_bytes);
	if (err != 0) {
		const size_t msg_size = 64;
		char msg[msg_size];
		sprintf_s(msg, msg_size, "read_unicode failed (%u)", err);
		botch(msg);
	}
	if (sjis_bytes != (ret-1)) {
		char msg[32];
		sprintf_s(msg, 31, "read %zd characters", ret);
		botch(msg);
	}
	return in_bytes;
}
static size_t count_sjis_bytes(wchar_t w_buff[], int count) {
	union { wchar_t w; char c[2]; } _u;
	size_t num_bytes = 0;
	for (int n = 0; n < count; n++) {
		_u.w = w_buff[n];
		++num_bytes;
		if (_u.c[1] != 0) {
			++num_bytes;
		}
	}
	return num_bytes;
}

int read_utf8(FILE* fp, byte* buff, int buff_size, int count) {
	byte* cp = buff;
	byte* ep = cp + buff_size - 1;
	byte b1, b2, b3, b4;
	int read_count = 0;
	while (read_count < count) {
		if (ep < cp + 1) botch("read_utf8: buffer ovrrun");
		b1 = read_byte(fp);
		if ((b1 & 0x80) == 0x00) {
			//printf("-- (1) %02X\n", b1);
			*cp++ = b1 & 0x7f;
			read_count += 1;
		} else if ((b1 & 0xe0) == 0xc0) {
			if (ep < cp + 1) botch("read_utf8: buffer ovrrun");
			b2 = read_byte(fp);
			//printf("-- (2) %02X %02X\n", b1, b2);
			read_count += 2;
			*cp++ = (b1 & 0x1c) >> 2;
			*cp++ = (b1 & 0x03) << 6 | (b2 & 0x3f);
		} else if ((b1 & 0xf0) == 0xe0) {
			if (ep < cp + 2) botch("read_utf8: buffer ovrrun");
			b2 = read_byte(fp);
			b3 = read_byte(fp);
			//printf("-- (3) %02X %02X %02X\n", b1, b2, b3);
			read_count += 3;
			*cp++ = (b1 & 0x0f) << 4 | (b2 & 0x3c) >> 2;
			*cp++ = (b2 & 0x03) << 6 | (b3 & 0x3f);
		} else if ((b1 & 0xf8) == 0xf0) {
			if (ep < cp + 3) botch("read_utf8: buffer ovrrun");
			b2 = read_byte(fp);
			b3 = read_byte(fp);
			b4 = read_byte(fp);
			//printf("-- (4) %02X %02X %02X %02X\n", b1, b2, b3, b4);
			read_count += 4;
			*cp++ = (b1 & 0x07) << 2 | (b2 & 0xc0) >> 4;
			*cp++ = (b2 & 0x0f) << 4 | (b3 & 0x3c) >> 2;
			*cp++ = (b3 & 0x03) << 6 | (b4 & 0x3f);
		} else {
			fprintf(stderr, "Botch: doubtful utf8: 0x%02X\n", b1);
			exit(-1);
		}
	}
	*cp = '\0';
	return read_count;
}

// end: reader.cpp
