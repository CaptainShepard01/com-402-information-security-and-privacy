# Binary Exploitation

Setup:

- install docker
- build the docker
- run the docker in privileged mode, mount this directory do /mnt (see run-docker.sh for linux), run bash
- insde of the docker: `tmux` `cd /mnt`  

exploit:

We provide a pwntools template to let you script your exploit in python. 
`python3 exploit.py GDB C1` to start c1 challenge and attach gdb to it.

## tmux

This will open another tmux pane. To navigate between the two panes use CTRL+B + arrow key up or down.

## pwntools

a python library to make exploit devleopment easier. (https://docs.pwntools.com/en/stable/)

things you might find useful:

p64(number): convert a number to bytes (8 bytes little endian), there is also (p32, p16, p8)

r.recvuntil(b"..."): wait until program has sent the b"..." string

p.sendline(payload): send payload:bytes to thetarget program

e = ELF(filepath): open an elf file e.sym: access the address/offset of symbols (ex. e.sym("main")). next(e.search(b"wow")): look for byte sequence wow in target program. 
