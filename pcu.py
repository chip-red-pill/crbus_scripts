import struct

def pcu_ext_mem_dump(start = 0, end = 0x10000, file_path):
    fo = open(file_path, "wb")
    for addr in range(start, end, 4):
        ipc.stateport.tap2iosf_tap0.sbreg(0, 0, 0x46a0, 0x46, 0, 4, 7, 0, addr)
        ipc.stateport.tap2iosf_tap0.sbreg(0, 0, 0x46a4, 0x46, 0, 4, 7, 0, 0x80000005)
        val = ipc.stateport.tap2iosf_tap0.sbreg(0, 0, 0x46a0, 0x46, 0, 4, 6)
        fo.write(struct.pack("<L", int(val)))
    fo.close()
