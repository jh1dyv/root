#ifndef	WRITER_H
#define	WRITER_H

#include "typedefs.h"

void print_link_flags(uint flags);
void print_file_attribute_flags(uint flags);
void print_link_info_flags(uint flags);
void print_device_type(uint flag);
char* printable_string(byte* string, int size);
void dump_bytes(byte* buff, int size, const char* trailer);

const int max_string_size = 1024;
const int max_buff_size = 1024;

#endif	// WRITER_H
