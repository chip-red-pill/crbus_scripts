import ipccli
ipc = ipccli.baseaccess()

def crbus_read(addr):
    glm0 = ipc.devs.glm_module0
    crbus_val = (0x3 << 79) | (addr << 65)
    ipc.irdrscan(glm0, 0xa8, 83, None, crbus_val, False)
    val = ipc.irdrscan(glm0, 0xa9, 83)
    data = (val & ((1 <<  0x41) - 1)) >> 1
    return data

def crbus_write(addr, val):
    glm0 = ipc.devs.glm_module0
    crbus_val = (0x1 << 80) | (addr << 65) | ((val &((1 << 64 ) - 1)) << 1)
    ipc.irdrscan(glm0, 0xa8, 83, None, crbus_val, False)
