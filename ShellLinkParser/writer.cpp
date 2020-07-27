// write.cpp
#include <stdio.h>
#include "typedefs.h"
#include "flagdefs.h"
#include "writer.h"
extern bool silent;
static void print_name(const char* name);

#define	print_flag_if_defined(data, flags) \
	if (flags(data)) { print_name(#flags); }

void print_link_flags(uint flags) {
	//if (silent) return;
	print_name(NULL);	// init
	print_flag_if_defined(flags, HasLinkTargetIDList);
	print_flag_if_defined(flags, HasLinkInfo);
	print_flag_if_defined(flags, HasName);
	print_flag_if_defined(flags, HasRelativePath);
	print_flag_if_defined(flags, HasWorkingDir);
	print_flag_if_defined(flags, HasArguments);
	print_flag_if_defined(flags, HasIconLocation);
	print_flag_if_defined(flags, IsUnicode);
	print_flag_if_defined(flags, ForceNoLinkInfo);
	print_flag_if_defined(flags, HasExpString);
	print_flag_if_defined(flags, RunInSeparateProcess);
	print_flag_if_defined(flags, Unused1);
	print_flag_if_defined(flags, HasDarwinID);
	print_flag_if_defined(flags, RunAsUser);
	print_flag_if_defined(flags, HasExpIcon);
	print_flag_if_defined(flags, NoPIDlAlias);
	print_flag_if_defined(flags, Unused2);
	print_flag_if_defined(flags, RunWithShimLayer);
	print_flag_if_defined(flags, ForceNoLinkTrack);
	print_flag_if_defined(flags, EnableTargetMeatadata);
	print_flag_if_defined(flags, DisableLinlPathTracking);
	print_flag_if_defined(flags, DisableKnownFolderTracking);
	print_flag_if_defined(flags, DisableKnownFolderAlias);
	print_flag_if_defined(flags, AllowLinkToLink);
	print_flag_if_defined(flags, UnaliasOnSave);
	print_flag_if_defined(flags, PreferEnvironmentPath);
	print_flag_if_defined(flags, KeeoLocalIDListForUNCTarget);
	printf("\n");
}

void print_file_attribute_flags(uint flags) {
	//if (silent) return;
	print_name(NULL);	// init
	print_flag_if_defined(flags, FILE_ATTRIBUTE_READONLY);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_HIDDEN);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_SYSTEM);
	print_flag_if_defined(flags, Reserved1);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_DIRECTORY);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_ARCHIVE);
	print_flag_if_defined(flags, Reserved2);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_NORMAL);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_TEMPORARY);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_SPARSE_FILE);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_REPARSE_POINT);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_COMPRESSED);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_OFFLINE);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_NOT_CONTENT_INDEXED);
	print_flag_if_defined(flags, FILE_ATTRIBUTE_ENCRYPTED);
	printf("\n");
}

void print_link_info_flags(uint flags) {
	//if (silent) return;
	print_name(NULL);	// init
	print_flag_if_defined(flags, VOLUME_ID_AND_LOCAL_BASE_PATH);
	print_flag_if_defined(flags, COMMON_NETWORK_RELATIVE_LINK_AND_PATH_SUFFIX);
	printf("\n");
}

void print_device_type(uint flag) {
	print_flag_if_defined(flag, DRIVE_UNKNOWN);
	print_flag_if_defined(flag, DRIVE_NO_ROOT_DIR);
	print_flag_if_defined(flag, DRIVE_REMOVABLE);
	print_flag_if_defined(flag, DRIVE_FIXED);
	print_flag_if_defined(flag, DRIVE_ERMOTE);
	print_flag_if_defined(flag, DRIVE_CDROM);
	print_flag_if_defined(flag, DRIVE_WRAMDISK);
	printf("\n");
}

static void print_name(const char* name) {
	static int count = 0;
	if (name == NULL) {
		count = 0;
		printf("%s", silent ? "\t" : "\t\t");
		return;
	}
	if (count++ == 5) {
		printf("\n%s", silent ? "\t" : "\t\t");
		//printf("\n\t");
		count = 0;
	}
	printf("%s, ", name);
}

char* printable_string(byte* string, int size) {
	static char buff[max_string_size+1];
	char* p = buff;
	if (size > max_string_size) {
		return (char*) "Botch: string too long\n";
	}
	for (int n = 0; n < size; n++) {
		char c = string[n];
		*p++ = (0x20 <= c && c <= 0x7e) ? c : ' ';
	}
	*p = '\0';
	return buff;
}

void dump_bytes(byte* buff, int size, const char* trailer) {
	if (silent) return;
	int block = 0, run = 0;
	for (int n = 0; n < size; n++) {
		if (++run > 4) {
			printf(" ");
			run = 1;
			if (++block >= 8) {
				printf("\n\t\t");
				block = 0;
			}
		}
		printf("%02X", buff[n]);
	}
	if (trailer != NULL) {
		printf("%s", trailer);
	}
}

// end: writer.cpp
