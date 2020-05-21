def ldat_array_read(pdat_reg, array_sel, bank_sel, dword_idx, fast_addr):
    crbus_write(pdat_reg + 1, 0x10000 | ((dword_idx & 0xf) << 12) | ((array_sel & 0xf) << 8) | (bank_sel & 0xf))
    crbus_write(pdat_reg, 0xc00000 | (fast_addr & 0xffff))
    crbus_write(pdat_reg + 1, 0)
    return crbus_read(pdat_reg + 2)

def ldat_array_write(pdat_reg, array_sel, bank_sel, dword_idx, fast_addr, val):
    crbus_write(pdat_reg + 4, val & 0xffffffff)
    crbus_write(pdat_reg + 5, (val >> 32) & 0xffff)
    crbus_write(pdat_reg + 1, 0x10000 | ((dword_idx & 0xf) << 12) | ((array_sel & 0xf) << 8) | (bank_sel & 0xf))
    crbus_write(pdat_reg, 0x800000 | (fast_addr & 0xffff))
    crbus_write(pdat_reg + 1, 0)

def ms_array_dump(array_sel, size):
    str_line = ""
    for fast_addr in range(0, size):
        if fast_addr and fast_addr % 4 == 0:
            print("%04x: %s" % ((fast_addr // 4 - 1) * 4, str_line))
            str_line = ""
        val = ldat_array_read(0x6a0, array_sel, 0, 0, fast_addr)
        str_line += " %012x" % val
    print("%04x: %s" % ((fast_addr // 4) * 4, str_line))

def ms_rom_dump():
    ms_array_dump(0, 0x8000)

def ms_irom_dump():
    ms_array_dump(1, 0x8000)

def ms_patch_consts_dump():
    ms_array_dump(2, 0x80)

def ms_match_patch_regs_dump():
    ms_array_dump(3, 0x20)

def ms_patch_ram_dump():
    ms_array_dump(4, 0x200)

def ms_match_patch_reg_write(addr, match_reg_val, patch_reg_val):
    ldat_array_write(0x6a0, 3, 0, 0, addr, (match_reg_val & 0xffff) | ((patch_reg_val & 0x7fff) << 16))

def ms_patch_ram_write(addr, val):
    ldat_array_write(0x6a0, 4, 0, 0, addr, val)
