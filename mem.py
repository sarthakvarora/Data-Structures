import numpy as np
from ctypes import *

class bit_vector: # Done

    def __init__(self, size): # Done
        self.size = size
    #     self.bitv = [0] * size
        # self.bitv = (c_ubyte*size)()
        # print(self.bitv)

    def create_vector(self, size):
        self.size = size
        self.bitv = [0] * self.size
        return self.bitv
        # initialize size "bits" in some python specific data structure.
        # it could be a list of bools may be
        # syntax you figure out a state = (False * size)[]
        # if it is False it is free
        # if it is True it is allocated. 

        # I use 0,1

        # this is a bit map.
        # instead of boolean I will use integers and use bit operators
        # to figure this.
        # because python supports large integers it could also be for eg.
        # int bits= 1 << (size+1) 
        # that means you could use simple bit logic  to figure if the bit is
        # set or not.
        # infat bit vector is a data structure 
        # using bits will be efficient for space. dont use integer. 
        # do not use any available classes.
        # you could also ctype. 
        # infact i suggest using c_ubyte the way we allocate linear bytes
        # allocate the byte for the bit vector ie. 128MB max. Do not hard code 
        # anything.

    def is_free(self, byteaddr): # Done
        return self.bitv[byteaddr]

    def set_bit(self, byteaddr): # Done
        self.bitv[byteaddr] = True

class mymemory:

    int32_max = (pow(2,31)-1)
    int32_min = -int32_max

    def __init__(self, memsize): # Done?
        memsize = memsize*1024*1024*8 # input in gb
        self.mem_arr = (c_ubyte*memsize)()
        # as defined in the content of getting a linear array of bytes.
        self.start=0xfffffffc00000000
        self.end = self.start+memsize
        self.size = memsize
        self.free = memsize
        # self.mem_alloc_state 
        Y = bit_vector(memsize//8)
        self.bitv = Y.create_vector(memsize//8)    #128MB for 1GB.
        # print(len(self.mem_arr))
        # print(len(self.bitv))
        # self.mem_int32_alloc
        # self.mem_int64_alloc
        # self.mem_alloc

        # initialize the allocation state.
        # helper bitvector.siz
        # pass


    def create_int(self, b1, b2, b3, b4): # Done
        b1,b2,b3,b4 = str(b1),str(b2),str(b3),str(b4)
        num = 0
        powr= 0
        for i in range(len(b4)-2,-1,-1):
            num = num + int(b4[i])*(2**(powr))
            powr = powr + 1

        for i in range(len(b3)-1,-1,-1):
            num = num + int(b3[i])*(2**(powr))
            powr = powr + 1

        for i in range(len(b2)-1,-1,-1):
            num = num + int(b2[i])*(2**(powr))
            powr = powr + 1

        for i in range(len(b1)-1,-1,-1):
            num = num + int(b1[i])*(2**(powr))
            powr = powr + 1
        return num

    def convert_ptr_to_int32(self, ptr): # Done.
        b1=self.mem_arr[ptr]
        b2=self.mem_arr[ptr+1]
        b3=self.mem_arr[ptr+2]
        b4=self.mem_arr[ptr+3]
        int32value = self.create_int(b1, b2, b3, b4)
        if b4%10 != 0:  # last digit is not zero.
            int32value = int32value*-1
        return int32value

    def convert_int32_to_bytes(self, int32value): # Done, needs fixes
        if int32value>=0:
            binary = [0]
        else:
            binary = [1]
        while int32value//2>0:
            rem = int32value%2
            int32value = int32value//2
            binary.append(rem)
        flip_binary = []
        for i in range(len(binary)):
            flip_binary.append(binary[-(i+1)])
        b11 = flip_binary[0:8]
        b21 = flip_binary[8:16]
        b31 = flip_binary[16:24]
        b41 = flip_binary[24:32]
        b1,b2,b3,b4 = "","","",""
        for i in b11:
            b1 = b1 + str(i)
        for i in b21:
            b2 = b2 + str(i)
        for i in b31:
            b3 = b3 + str(i)
        for i in b41:
            b4 = b4 + str(i)
        return b1, b2, b3, b4
        
    def is_valid_ptr(self, ptr):          # Done
        if ptr > self.start and ptr < self.start + self.memsize:
            # if it lies within the array basically
            ptr_valid = True
        else:
            ptr_valid = False
        return ptr_valid

    def mem_alloc(self, nbytes):              # Done
        for i in range(0,len(self.bitv)):
            if np.all((self.bitv[i:i+nbytes] == 0)):
                ptr = self.start + i
                break
            else:
                ptr = -1
        self.free -= nbytes
        return ptr

    def load_int32(self, ptr):                # Done
        if self.is_valid_ptr(ptr) == False:
            print("pointer invalid.")
        else:
            return self.convert_ptr_to_int32(ptr)

    def store_int32(self, value, ptr=None): # Done
        if (ptr == None):
            ptr = self.mem_alloc(4)
            # self.mem_int32_alloc += 4         #What does this do?

        if (value > self.int32_max and value < self.int32_min):
            print("Error: That can't fit into 32 bits.")
        else:
            self.b1,self.b2,self.b3,self.b4 = self.convert_int32_to_bytes(value)
            #store the bytes in a little endian way to the memory array.
            # self.mem_arr[ptr+0-self.start] = self.b1
            # self.mem_arr[ptr+1-self.start] = self.b2
            # self.mem_arr[ptr+2-self.start] = self.b3
            # self.mem_arr[ptr+3-self.start] = self.b4
            self.mem_arr[ptr+0] = int(self.b1)
            self.mem_arr[ptr+1] = int(self.b2)
            self.mem_arr[ptr+2] = int(self.b3)
            self.mem_arr[ptr+3] = int(self.b4)

        # if value < 0:
            # set the 8th bit of b4 to indicate it is negative. Done already

# repeat  the above for 

    # def load_int64()
    # def store_int64()
    # def convert_ptr_to_int64()
    # def convert_int64_to_bytes()

X = mymemory(1)
X.store_int32(255)
print(X[0:3])
