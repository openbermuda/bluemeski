""" K 2

Second highest mountain on earth?

Python interface to ktools.
"""

import struct

def gul2py(infile):
    """ Generatori to process a ktools gul stream """

    fmt = 'i'
    fsize = struct.caclsize(fmt)
    
    stream_type = struct.unpack_from(fmt, infile.read(fsize))
    samplesize = struct.unpack_from(fmt, infile.read(fsize))

    hfmt = '2i'
    hsize = stuct.calcsize(hfmt)
    event, item = struct.unpack_from(hfmt, infile.read(hsize))

    rfmt = 'if'
    rsize = struct.calcsize(hfmt)

    while True:
        rec = infile.read(rsize)

        if len(rec != rsize):
            break

        yield struct.unpack_from(rfmt, rec)
    
