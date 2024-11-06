FROM aflplusplus/aflplusplus

RUN git clone https://github.com/kdsjZh/COM402-Testing-Lab /COM402-Testing-Lab 

ENV AFL_PATH "/AFLplusplus"

RUN cd /COM402-Testing-Lab/demo/ex1 && \
    CC=gcc make ex1 && \
    cd /COM402-Testing-Lab/demo/ex2 && \
    CC=afl-cc make ex2 && \
    cd /COM402-Testing-Lab/demo/ex3 && \
    CC=afl-cc make ex3 && mv ex3 ex3.afl && \
    CC=afl-cc AFL_LLVM_CMPLOG=1 make ex3 && mv ex3 ex3.cmplog && \
    cd /COM402-Testing-Lab/demo/ex4 && \
    CC=afl-cc AFL_USE_ASAN=1 make ex4 
