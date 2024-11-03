# Binary Exploitation

Setup:

- install docker https://docs.docker.com/engine/install/
- build the docker (see build-docker.sh)
- run the docker in privileged mode, mount this directory do /mnt (see run-docker.sh for linux)
- insde of the docker run: `tmux` and `cd /mnt`  

exploit:

We provide a pwntools template to let you script your exploit in python. 
`python3 exploit.py GDB C0` to start c0 challenge and attach gdb to it.

## Goal

The goal of each challenge c0,c1,c2,c3 is to either make the program print (you win!) or hijack code execution and execute /bin/sh (shell). All programs have a buffer overflow vulnerability that you can try to exploit.

## tmux

This will open another tmux pane. We use this alongside exploit.py so you have two panes, one with the program output and one with gdb. To navigate between the two panes use CTRL+B + arrow key up or down.

## pwntools

a python library to make exploit devleopment easier. (https://docs.pwntools.com/en/stable/)

things you might find useful:

p64(number): convert a number to bytes (8 bytes little endian), there is also (p32, p16, p8)

r.recvuntil(b"..."): wait until program has sent the b"..." string

p.sendline(payload): send payload:bytes to thetarget program

e = ELF(filepath): open an elf file e.sym: access the address/offset of symbols (ex. e.sym("main")). next(e.search(b"wow")): look for byte sequence wow in target program. 

## GDB

a debugger to help you figure out  what is happening.

x/20gx [address] to print memory around an address
s/n: step to the next line in the program (n steps over function calls)
si/ni: stpe to the next instruction
