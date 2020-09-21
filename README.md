# bitmap-rle-compressor

## A highly unoptimized RLE bitmap compression tool

Created specifically for a course in which I had to create bitmaps from columns, and then compress them using a method described in the textbook. For the curious, it's "Database Systems: The Complete Book (2nd Edition)" ISBN-13: 978-0131873254, in Section 14.7.

### Usage: 
Call the program using Python 2 or 3, with the data to be converted as space-separated values.

Example: python bmp_rle.py 1024 512 512 1024 512 1024

### Optional arguments:
-u (--uncomp) or -c (--comp) to generate only the [un]compressed output.

-p (--pprint) for pretty-printed output.

-t (--test) for a test with known data.

-h (--help) for an argparse helper.