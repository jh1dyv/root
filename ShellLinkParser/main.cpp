//
#define	_CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <locale.h>
#include <string.h>
#include <iostream>
#include <string>
#include <wchar.h>
#include <io.h>
#include <fcntl.h>
//#include <cstdarg>
#include <assert.h>
#include "typedefs.h"
#include "flagdefs.h"
#include "reader.h"
#include "writer.h"

// globals
const char* prog = "GetLinkTarget";
long fpos = 0;
bool silent = true;
bool verbose = false;

// locals
static char msg[max_buff_size+1];	// for error message
static byte buff[max_buff_size+1];
static void botch(const char* msg);
static void usage(void);

int main(int argc, char* argv[], char* envv) {

	// get command line arguments
	if (argc > 1 && strcmp(argv[1], "-v") == 0) {
		verbose = 1;
		argc--;
		argv++;
	}
	if (argc != 2) {
		usage();
	}
	char* infile = argv[1];
	silent = !verbose;
	if (verbose)
		printf("infile: %s\n", infile);

	// open input file
	FILE* fp = fopen(infile, "rb");
	if (fp == NULL) {
		fprintf(stderr, "%s: can't open file \"%s\"\n", prog, infile);
		exit(1);
	}
	fseek(fp, 0L, SEEK_END);
	long eof = ftell(fp);		// tells truth

	// -------------------------------------------------------------
	//  SHELL_LINK_HEADER
	// -------------------------------------------------------------
	fseek(fp, fpos, SEEK_SET);
	printf("\n");
	printf("---- SHELL_LINK_HEADER at 0x%04X --\n", fpos);

	// HeaderSize (4 bytes)
	uint header_size = read_uint(fp);
	if (verbose) {
		int size = header_size;
		printf("  HeaderSize:	%d (0x%X) \n", size, size);
	}

	// LinkCLSID (16 bytes)
	uint link_clsid_u = read_uint(fp);
	word link_clsid_w0 = read_word(fp);
	word link_clsid_w1 = read_word(fp);
	byte link_clsid_b0[2];
	read_bytes(fp, link_clsid_b0, 2);
	byte link_clsid_b1[6];
	read_bytes(fp, link_clsid_b1, 6);
	if (verbose) {
		printf("  LinkCLSID:	%08X-%04X-%04x-",
			link_clsid_u, link_clsid_w0, link_clsid_w1);
		dump_bytes(link_clsid_b0, 2, "-");
		dump_bytes(link_clsid_b1, 6, "\n");
	}

	// LinkFlags (4 bytes)
	uint link_flags;
	link_flags = read_uint(fp);
	if (!silent) {
		printf("  LinkFlags:	%08X\n", link_flags);
	}
	print_link_flags(link_flags);

	// FileAttributeFlags (4 bytes)
	uint file_attribute_flags;
	file_attribute_flags = read_uint(fp);
	if (verbose) {
		printf("  FileAttributeFlags:	%08X\n\t\t", file_attribute_flags);
	}
	print_file_attribute_flags(file_attribute_flags);

	// CreationTime, AccessTime, WriteTime (8 bytes for each)
	byte creation_time[8], access_time[8], write_time[8];
	read_bytes(fp, creation_time, 8);
	read_bytes(fp, access_time, 8);
	read_bytes(fp, write_time, 8);
	if (verbose) {
		printf("  CreationTime:	");
		dump_bytes(creation_time, 8, "\n");
		printf("  AccessTime:	");
		dump_bytes(creation_time, 8, "\n");
		printf("  WriteTime:	");
		dump_bytes(creation_time, 8, "\n");
	}

	// FileSize (4 bytes)	-> 10344 (0x2868) bytes
	uint file_size = read_uint(fp);
	if (verbose) {
		printf("  FileSize:	%08X (%d)\n", file_size, file_size);
	}
	
	// IconIndex (4bytes)
	uint icon_index = read_uint(fp);
	if (verbose) {
		printf("  IconIndex:	%d\n", icon_index);
	}

	// ShowCommand (4bytes)
	uint show_command = read_uint(fp);
	if (verbose) {
		printf("  ShowCommand:	%08X", show_command);
		if (show_command == 0x00000001) printf(" SW_SHOWNORMAL\n");
		if (show_command == 0x00000003) printf(" SW_SHOWMAXIMIZED\n");
		if (show_command == 0x00000007) printf(" SW_SHOWMINNOACTIVE\n");
	}

	// HotKey (2 bytes)
	byte hot_key[2];
	read_bytes(fp, hot_key, 2);
	if (verbose) {
		printf("  HotKey:	");
		dump_bytes(hot_key, 2, "\n");
	}

	// Reserved1 (2 bytes), Reserved2 (4 bytes), Reserved3 (4 bytes)
	byte reserved1[2], reserved2[4], reserved3[4];
	read_bytes(fp, reserved1, 2);
	read_bytes(fp, reserved2, 4);
	read_bytes(fp, reserved3, 4);
	if (verbose) {
		printf("  Reserved:	");
		dump_bytes(reserved1, 2, " ");
		dump_bytes(reserved2, 4, " ");
		dump_bytes(reserved3, 4, "\n");
	}

	// -------------------------------------------------------------
	//  LINKTARGET_IDLIST
	// -------------------------------------------------------------
	assert(fpos == ftell(fp));
	//fseek(fp, fpos, SEEK_SET);
	if (HasLinkTargetIDList(link_flags)) {
		printf("\n");
		printf("---- LINKTARGET_IDLIST at 0x%04X --\n", fpos);

		// IDListSize
		word id_list_size = read_word(fp);
		if (verbose) {
			int size = id_list_size;
			printf("  LinkTaregtIDList size: %d (0x%x) \n", size, size);
		}

		// ItemIDSize
		const int max_item_id_size = 1024;
		byte item_id[max_item_id_size];
		while (id_list_size > 0) {
			word item_id_size = read_word(fp);
			if (item_id_size == 0) {
				if (verbose) {
					printf("  ---- TerminalID ----\n");
				}
				break;
			}
			printf("  ---- ItemID ----\n");
			id_list_size -= item_id_size;
			item_id_size -= sizeof(word);
			if (verbose) {
				printf("    ItemIDSize size: 2+%d", item_id_size);
				printf(" (%d left)\n", id_list_size);
			}
			if (item_id_size > max_item_id_size) {
				sprintf(msg, "item id siez exceed %d", max_item_id_size);
				botch((const char*) msg);
			}
			read_bytes(fp, item_id, item_id_size);
			if (verbose) {
				printf("    Data:	");
				dump_bytes(item_id, item_id_size, "\n");
			}
		}

	}

	// -------------------------------------------------------------
	//  LINKINFO
	// -------------------------------------------------------------
	assert(fpos == ftell(fp));
	//fseek(fp, fpos, SEEK_SET);
	if (HasLinkInfo(link_flags)) {
		printf("\n");
		printf("---- LINKINFO at 0x%04X --\n", fpos);
		bool unicode = false;
		long block_top = fpos;
#define	OFFSET	(fpos - block_top)

		// LinkInfoSize
		// LinkInfoHeaderSize
		uint link_info_size = read_uint(fp);
		uint link_info_header_size = read_uint(fp);
		if (verbose) {
			int size1 = link_info_size;
			int size2 = link_info_header_size;
			printf("  LinkInfoSize:	 %d (0x%x)\n", size1, size1);
			printf("  LinkInfoHeaderSize: %d (0x%x)", size2, size2);
			const char* msg1 = "Offsets to the optional fields are";
			const char* msg2 = " ??";
			const char* msg3 = " specified";
			if (link_info_header_size == 0x0000001c) msg2 = " not";
			if (link_info_header_size >= 0x00000024) msg2 = "";
			printf(" (%s%s%s)\n", msg1, msg2, msg3);
		}

		// LinkInfoFlags
		uint link_info_flags = read_uint(fp);
		if (verbose) {
			printf("  LinkInfoFlags: %08X\n", link_info_flags);
		}
		print_link_info_flags(link_info_flags);

		// VolumeIDOffset
		// LocalBasePathOffset
		// CommonNetworkRelativeLinkOffset
		// CommonPathSuffixOffset
		uint volume_id_offset = read_uint(fp);
		uint local_base_path_offset = read_uint(fp);
		uint common_network_relative_link_offset = read_uint(fp);
		uint common_path_suffix_offset = read_uint(fp);
		if (verbose) {
			printf("  VolumeIDOffset:         %08X\n", volume_id_offset);
			printf("  LocalBasePathOffset:    %08X\n", local_base_path_offset);
			printf("  CommonNetworkRelativeLinkOffset: %08X\n", common_network_relative_link_offset);
			printf("  CommonPathSuffixOffset: %08X\n", common_path_suffix_offset);
		}
		if (!VOLUME_ID_AND_LOCAL_BASE_PATH(link_info_flags)) {
			if (volume_id_offset != 0)
				botch("VolumeIDOffset MUST be zero");
			if (local_base_path_offset != 0)
				botch("LocalBasePathOffset MUST be zero");
		}
		if (!COMMON_NETWORK_RELATIVE_LINK_AND_PATH_SUFFIX(link_info_flags)) {
			if (common_network_relative_link_offset != 0)
				botch("CommonNetwrokRelativeLinkOffset MUST be zero");
		}

		// LocalBasePathOffsetUnicode (optional)
		if (link_info_header_size >= 0x00000024) {
			uint local_base_path_offset_unicode = read_uint(fp);
			if (verbose) {
				printf("  LocalBasePathOffsetUnicode: %08X\n",
						local_base_path_offset_unicode);
			}
			if (!VOLUME_ID_AND_LOCAL_BASE_PATH(link_info_flags) &&
				local_base_path_offset_unicode != 0) {
				botch("LocalBasePathOffsetUnicode MUST be zero");
			}
		}

		// CommonPathSuffixOffsetUnicode (optional)
		if (link_info_header_size >= 0x00000024) {
			uint common_path_suffix_offset_unicode = read_uint(fp);
			if (verbose) {
				printf("  CommonPathSuffixOffsetUnicode: %08X\n",
						common_path_suffix_offset_unicode);
			}
		}

		// VolumeID (variable)
		if (VOLUME_ID_AND_LOCAL_BASE_PATH(link_info_flags)) {
			printf("\n");
			printf("  ---- VolumeID at 0x%X --\n", OFFSET);
			long start = fpos;

			// VolueIDSize
			if (volume_id_offset != OFFSET) {
				botch("offset - VolumeID");
			}
			uint volume_id_size = read_uint(fp);
			if (verbose) {
				printf("    VolumeIDSize: %d\n", volume_id_size);
			}
			if (volume_id_size <= 0x10) {
				botch("VolumeIDSize not greater than 0x10");
			}

			// DeviceType
			uint device_type = read_uint(fp);
			if (verbose) {
				printf("    DeviceType: %08X ", device_type);
				print_device_type(device_type);
			}

			// DeviceSerialNumber
			uint device_serial_number = read_uint(fp);
			if (verbose) {
				printf("    DeviceSerialNumber: %d\n", device_serial_number);
			}

			// VolumeLabelOffset
			uint volume_label_offset = read_uint(fp);
			if (verbose) {
				printf("    VolumeLabelOffset: %08X", volume_label_offset);
				if (volume_label_offset == 0x14)
					printf(" ignored");
				printf(" \n");
			}
			unicode = false;

			// VolumeLabelOffsetUnicode
			if (volume_label_offset == 0x14) {
				volume_label_offset= read_uint(fp);
				if (verbose) {
					printf("    VolumeLabelOffsetUnicode: %08X\n",
						volume_label_offset);
				}
				unicode = true;
			}

			// Data (variable)
			int data_size = volume_id_size - (int) (fpos - start);
			byte data[1024+1];
			read_bytes(fp, data, data_size);
			data[data_size] = '\0';
			if (verbose) {
				printf("    Data: (%d) \"%s\"\n", data_size, data);
			}
		}

		// LocalBasePath (varible)
		if (VOLUME_ID_AND_LOCAL_BASE_PATH(link_info_flags) && !unicode) {
			printf("\n");
			printf("  ---- LocalBasePath at 0x%X --\n", OFFSET);

			byte path[1024];
			int size = read_asciz(fp, path, 1024);
			printf("    LocalBasePath: (%d) \"%s\"\n", size, path);
		}

		// CommonNetworRelativeLink (variable)
		if (COMMON_NETWORK_RELATIVE_LINK_AND_PATH_SUFFIX(link_info_flags)) {
			printf("\n");
			printf("  ---- CommonNetworkRelative Link at 0x%X --\n", OFFSET);
			
			printf("**** NOT IMPLEMENTED ***\n");
			return 0;
		}

		// CommonPathSuffix (variable)
		if (VOLUME_ID_AND_LOCAL_BASE_PATH(link_info_flags) && !unicode) {
			printf("\n");
			printf("  ---- CommonPathSuffix at 0x%X --\n", OFFSET);

			byte path_suffix[1024];
			int size = read_asciz(fp, path_suffix, 1024);
			printf("    LocalBasePathSuffix: (%d) \"%s\"\n",
						size, path_suffix);
		}

		// LocalBasePathUnicode (variable)
		if (unicode) {
			printf("\n");
			printf("  ---- LocalBasePathUnicode at 0x%X --\n", OFFSET);

			byte path_unicode[1024];
			int size = read_asciz(fp, path_unicode, 1024);
			if (verbose) {
				printf("    LocalBasePathUnicode: (%d) \"%s\"\n",
						size, path_unicode);
			}
		}

		// CommonPathSuffixUnicode (variable)
		if (unicode) {
			printf("\n");
			printf("  ---- LocalBaseSuffixUnicode at 0x%X --\n", OFFSET);

			byte suffix_unicode[1024];
			int size = read_asciz(fp, suffix_unicode, 1024);
			if (verbose) {
				printf("    LocalBaseSuffixUnicode: (%d) \"%s\"\n",
						size, suffix_unicode);
			}
		}
	}

	// -------------------------------------------------------------
	//  STRING_DATA
	// -------------------------------------------------------------
	assert(fpos == ftell(fp));
	//fseek(fp, fpos, SEEK_SET);
	printf("\n");
	printf("---- STRING_DATA at 0x%04X --\n", fpos);
	if (IsUnicode(link_flags)) {
		// ロケール変更
		std::wcout.imbue(std::locale("", std::locale::ctype));
 		setlocale(LC_ALL, "Japanese");
		//printf("using unicode\n");
	}
	int nbytes;

	// NAME_STRING
	if (HasName(link_flags)) {
		byte name_string[max_string_size+1];
		word count_characters = read_word(fp);
		if (count_characters > max_string_size) {
			sprintf(msg, "name string too long (%d)", count_characters);
			botch(msg);
		}
		nbytes = read_unicode(fp, name_string, max_string_size, count_characters);
		printf("  -- NameString: (%d) ", count_characters);
		printf("%s\n", name_string);
		if (verbose) {
			printf("\t\t");
			dump_bytes(name_string, count_characters+1, "\n");
		}
	}

	// RELATIVE_PATH
	if (HasRelativePath(link_flags)) {
		byte relative_path[max_string_size+1];
		word count_characters = read_word(fp);
		if (count_characters > max_string_size) {
			fprintf(stderr, "Botch: relative path size exceed %d\n",
				max_string_size);
			return -1;
		}
		nbytes = read_unicode(fp, relative_path, max_string_size, count_characters);
		printf("  -- RelativePath: (%d) ", count_characters);
		printf("%s\n", relative_path);
		if (verbose) {
			printf("\t\t");
			dump_bytes(relative_path, count_characters, "\n");
		}
	}

	// WORKING_DIR
	if (HasWorkingDir(link_flags)) {
		byte working_dir[max_string_size+1];
		word count_characters = read_word(fp);
		if (count_characters > max_string_size) {
			fprintf(stderr, "Botch: working dir size exceed %d\n",
				max_string_size);
			return -1;
		}
		nbytes = read_unicode(fp, working_dir, max_string_size, count_characters);
		printf("  -- WorkingDir: (%d) ", count_characters);
		printf("%s\n", working_dir);
		if (verbose) {
			printf("\t\t");
			dump_bytes(working_dir, count_characters, "\n");
		}
	}

	// COMMAND_LINE_ARGUMENTS
	if (HasArguments(link_flags)) {
		byte command_line_arguments[max_string_size+1];
		word count_characters = read_word(fp);
		if (count_characters > max_string_size) {
			fprintf(stderr, "Botch: command line arguments  size exceed %d\n",
				max_string_size);
			return -1;
		}
		nbytes = read_unicode(fp, command_line_arguments, max_string_size, count_characters);
		printf("  -- CommandLineArguments: (%d) ", count_characters);
		printf("%s\n", command_line_arguments);
		if (verbose) {
			printf("\t\t");
			dump_bytes(command_line_arguments, count_characters, "\n");
		}
	}

	// ICON_LOCATION
	if (HasIconLocation(link_flags)) {
		byte icon_location[max_string_size+1];
		word count_characters = read_word(fp);
		if (count_characters > max_string_size) {
			fprintf(stderr, "Botch: icon location size exceed %d\n",
				max_string_size);
			return -1;
		}
		nbytes = read_unicode(fp, icon_location, max_string_size, count_characters);
		printf("  -- IconLocation: (%d) ", count_characters);
		printf("%s\n", icon_location);
		if (verbose) {
			printf("\t\t");
			dump_bytes(icon_location, count_characters, "\n");
		}
	}

	// -------------------------------------------------------------
	//  EXTRA_DATA
	// -------------------------------------------------------------
	assert(fpos == ftell(fp));
	//fseek(fp, fpos, SEEK_SET);
	printf("\n");
	printf("---- EXTRA_DATA at 0x%04X --\n", ftell(fp));
#define	DATA_SIZE	((int) (block_size - 2*sizeof(uint)))
	
	int n = 0;
	while (1) {
		uint block_size = read_uint(fp);
		if (block_size < 4) {
			printf("  -- TERMINAL_BLOCK (%d)--\n", (int) block_size);
			break;
		}
		uint block_signature = read_uint(fp);
		if (verbose) {
			printf("  block: size %08X, signature %08X at %04IX\n",
				block_size, block_signature, fpos-2*sizeof(uint));
		}
		if (block_size == 0x000000CC && block_signature == 0xA0000002) {
			printf("  -- ConsoleDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size == 0x0000000C && block_signature == 0xA0000004) {
			printf("  -- ConsoleFEDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size == 0x00000314 && block_signature == 0xA0000006) {
			printf("  -- DarwinDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size == 0x00000314 && block_signature == 0xA0000001) {
			printf("  -- EnvironmentVariableDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size == 0x00000314 && block_signature == 0xA0000007) {
			printf("  -- IconEnvironmentDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size == 0x0000001C && block_signature == 0xA000000B) {
			printf("  -- KnownFolderDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size >= 0x0000000C && block_signature == 0xA0000009) {
			printf("  -- PropertyStoreDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size >= 0x00000088 && block_signature == 0xA0000008) {
			printf("  -- ShimDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size == 0x00000010 && block_signature == 0xA0000005) {
			printf("  -- SpecialFolderDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size == 0x00000060 && block_signature == 0xA0000003) {
			printf("  -- TrackerDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else if (block_size >= 0x0000000A && block_signature == 0xA000000C) {
			printf("  -- VistaAndAboveIDListDataBlock --\n");
			/* NOT IMPLEMENTED */
			read_bytes(fp, buff, DATA_SIZE);
		}
		else {
			printf("  -- UNKNOWN_BLOCK --\n");
		}
		if (fpos >= eof) {
			sprintf_s(msg, max_buff_size, "fp (%X) exceeds eof (%X)\n", 
				fpos, eof);
			botch(msg);
		}
	}

	// -------------------------------------------------------------
	//  end of file
	// -------------------------------------------------------------
	printf("\n");
	printf("---- eof at 0x%04X --\n", fpos);
	fclose(fp);
	return 0;
}

static void botch(const char* msg) {
	fprintf(stderr, "Botch: %s\n", msg);
	exit(-1);
}
static void usage() {
	fprintf(stderr, "Usage: %s file\n", prog);
	exit(1);
}

// end: main.cpp
