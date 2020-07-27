#ifndef	FLAGDEFS_H
#define	FLAGDEFS_H

// -----------------------------------------------------------------------------
//  LinkFlags
// -----------------------------------------------------------------------------
#define	HasLinkTargetIDList(flags)		(flags & 0x00000001)	// A
#define	HasLinkInfo(flags)			(flags & 0x00000002)	// B
#define	HasName(flags)				(flags & 0x00000004)	// C
#define	HasRelativePath(flags)			(flags & 0x00000008)	// D
#define	HasWorkingDir(flags)			(flags & 0x00000010)	// E
#define	HasArguments(flags)			(flags & 0x00000020)	// F
#define	HasIconLocation(flags)			(flags & 0x00000040)	// G
#define	IsUnicode(flags)			(flags & 0x00000080)	// H
#define	ForceNoLinkInfo(flags)			(flags & 0x00000100)	// I
#define	HasExpString(flags)			(flags & 0x00000200)	// J
#define	RunInSeparateProcess(flags)		(flags & 0x00000400)	// K
#define	Unused1(flags)				(flags & 0x00000800)	// L
#define	HasDarwinID(flags)			(flags & 0x00001000)	// M
#define	RunAsUser(flags)			(flags & 0x00002000)	// N
#define	HasExpIcon(flags)			(flags & 0x00004000)	// O
#define	NoPIDlAlias(flags)			(flags & 0x00008000)	// P
#define	Unused2(flags)				(flags & 0x00010000)	// Q
#define	RunWithShimLayer(flags)			(flags & 0x00020000)	// R
#define	ForceNoLinkTrack(flags)			(flags & 0x00040000)	// S
#define	EnableTargetMeatadata(flags)		(flags & 0x00080000)	// T
#define	DisableLinlPathTracking(flags)		(flags & 0x00100000)	// U
#define	DisableKnownFolderTracking(flags)	(flags & 0x00200000)	// V
#define	DisableKnownFolderAlias(flags)		(flags & 0x00400000)	// W
#define	AllowLinkToLink(flags)			(flags & 0x00800000)	// X
#define	UnaliasOnSave(flags)			(flags & 0x01000000)	// Y
#define	PreferEnvironmentPath(flags)		(flags & 0x02000000)	// Z
#define	KeeoLocalIDListForUNCTarget(flags)	(flags & 0x04000000)	// AA

// -----------------------------------------------------------------------------
//  FileAttributesFlags
// -----------------------------------------------------------------------------
#define	FILE_ATTRIBUTE_READONLY(flags)		(flags & 0x00000001)	// A
#define	FILE_ATTRIBUTE_HIDDEN(flags)		(flags & 0x00000002)	// B
#define	FILE_ATTRIBUTE_SYSTEM(flags)		(flags & 0x00000004)	// C
#define	Reserved1(flags)			(flags & 0x00000008)	// D
#define	FILE_ATTRIBUTE_DIRECTORY(flags)		(flags & 0x00000010)	// E
#define	FILE_ATTRIBUTE_ARCHIVE(flags)		(flags & 0x00000020)	// F
#define	Reserved2(flags)			(flags & 0x00000040)	// G
#define	FILE_ATTRIBUTE_NORMAL(flags)		(flags & 0x00000080)	// H
#define	FILE_ATTRIBUTE_TEMPORARY(flags)		(flags & 0x00000100)	// I
#define	FILE_ATTRIBUTE_SPARSE_FILE(flags)	(flags & 0x00000200)	// J
#define	FILE_ATTRIBUTE_REPARSE_POINT(flags)	(flags & 0x00000400)	// K
#define	FILE_ATTRIBUTE_COMPRESSED(flags)	(flags & 0x00000800)	// L
#define	FILE_ATTRIBUTE_OFFLINE(flags)		(flags & 0x00001000)	// M
#define	FILE_ATTRIBUTE_NOT_CONTENT_INDEXED(flags)\
						(flags & 0x00002000)	// N
#define	FILE_ATTRIBUTE_ENCRYPTED(flags)		(flags & 0x00004000)	// O

// -----------------------------------------------------------------------------
//  FileAttributesFlags
// -----------------------------------------------------------------------------
#define	VOLUME_ID_AND_LOCAL_BASE_PATH(flags)	(flags & 0x00000001)	// A
#define	COMMON_NETWORK_RELATIVE_LINK_AND_PATH_SUFFIX(flags)\
						(flags & 0x00000002)	// B

// -----------------------------------------------------------------------------
//  DeviceType
// -----------------------------------------------------------------------------
#define	DRIVE_UNKNOWN(flags)			(flags == 0x00000000)
#define	DRIVE_NO_ROOT_DIR(flags)		(flags == 0x00000001)
#define	DRIVE_REMOVABLE(flags)			(flags == 0x00000002)
#define	DRIVE_FIXED(flags)			(flags == 0x00000003)
#define	DRIVE_ERMOTE(flags)			(flags == 0x00000004)
#define	DRIVE_CDROM(flags)			(flags == 0x00000005)
#define	DRIVE_WRAMDISK(flags)			(flags == 0x99999996)

#endif	FLAGDEFS_H
