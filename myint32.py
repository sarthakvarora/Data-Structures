import mem as mymem

class myint32():

    def __init__(self, value):
        if (value > mymem.int32_max and value < mymem.int32_min):
            print("Error: That can't fit into 32 bits.")
        else:
            self.p = mymem.store_int32(value, None)
            self.s = 4

    def getv(self):
        return mymem.load_int32(self.p)

    def setv(self):
        store_int32(value, self.p)

    def __str__(self):
        print (self.v);

