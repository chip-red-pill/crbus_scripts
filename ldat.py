#EXTREMELY UNSTABLE!!!
#Please use it only if you understand what you are doing!!!

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

def ms_array_write_no_atomic(array_sel, bank_sel, dword_idx, fast_addr, val):
    ldat_array_write(0x6a0, array_sel, bank_sel, dword_idx, fast_addr, val)

def ms_patch_ram_write_no_atomic(addr, val):
    ms_array_write_no_atomic(4, 0, 0, addr, val)

def ms_match_patch_write_no_atomic(addr, val):
    ms_array_write_no_atomic(3, 0, 0, addr, val)

def ms_const_write_no_atomic(addr, val):
    ms_array_write_no_atomic(2, 0, 0, addr, val)

#Microcode CPUID[80000002] leaf patcher (uCode version: 0x40)
def fix_cpuid_80000002():
    ms_debug_defeature_val = crbus_read(0x38c)
    crbus_write(0x38c, 0)
    ms_match_patch_write_no_atomic(0x3e, 0x3e4221b5)
    ms_match_patch_write_no_atomic(4, 0x3e4c21bd)
    ms_patch_ram_write_no_atomic(0x21+0x80*0, 0xc008433e000b) # rax:= MOV_DSZ32(0x00006f43)
    ms_patch_ram_write_no_atomic(0x21+0x80*1, 0x002410020220) # rax:= SHL_DSZ32(rax, 0x00000010)
    ms_patch_ram_write_no_atomic(0x21+0x80*2, 0x80085b57700b) # tmp7:= MOV_DSZ32(0x0000755b)
    ms_patch_ram_write_no_atomic(0x22+0x80*0, 0x0008204b808a) # tmp8:= MOV_DSZ32(0x00005220)
    ms_patch_ram_write_no_atomic(0x22+0x80*1, 0x000100020de0) # rax:= OR_DSZ32(rax, tmp7)
    ms_patch_ram_write_no_atomic(0x22+0x80*2, 0x002410023238) # rbx:= SHL_DSZ32(tmp8, 0x00000010)
    ms_patch_ram_write_no_atomic(0x23+0x80*0, 0x00086417700b) # tmp7:= MOV_DSZ32(0x00006564)
    ms_patch_ram_write_no_atomic(0x23+0x80*1, 0x000100023de3) # rbx:= OR_DSZ32(rbx, tmp7)
    ms_patch_ram_write_no_atomic(0x23+0x80*2, 0x80082d43700a) # tmp7:= MOV_DSZ32(0x0000502d)
    ms_patch_ram_write_no_atomic(0x24+0x80*0, 0x00086513800b) # tmp8:= MOV_DSZ32(0x00002055)
    ms_patch_ram_write_no_atomic(0x24+0x80*1, 0x002410037237) # tmp7:= SHL_DSZ32(tmp7, 0x00000010)
    ms_patch_ram_write_no_atomic(0x24+0x80*2, 0x800100021df8) # rcx:= OR_DSZ32(tmp8, tmp7)
    ms_patch_ram_write_no_atomic(0x25+0x80*0, 0x40086933700b) # tmp7:= MOV_DSZ32(0x00006c69)
    ms_patch_ram_write_no_atomic(0x25+0x80*1, 0x40086c76200a) # rdx:= MOV_DSZ32(0x00005d6c)
    ms_patch_ram_write_no_atomic(0x25+0x80*2, 0x002410022222) # rdx:= SHL_DSZ32(rdx, 0x00000010)
    ms_patch_ram_write_no_atomic(0x26+0x80*0, 0x000100022de2) # rdx:= OR_DSZ32(rdx, tmp7)
    ms_patch_ram_write_no_atomic(0x26+0x80*1, 0)
    ms_patch_ram_write_no_atomic(0x26+0x80*2, 0)
    ms_const_write_no_atomic(0x21, 0x0000300000c0)
    ms_const_write_no_atomic(0x22, 0x0000300000c0)
    ms_const_write_no_atomic(0x23, 0x0000300000c0)
    ms_const_write_no_atomic(0x24, 0x0000300000c0)
    ms_const_write_no_atomic(0x25, 0x0000300000c0)
    ms_const_write_no_atomic(0x26, 0x197ec80)
    crbus_write(0x38c, ms_debug_defeature_val)
