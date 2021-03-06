import simpy
import random

class customer:
    # simulates customer arrival and service
    # sorry for misleading name OO is hard and
    # so is simpy

    waitTime = 0.0      #total wait time for all customers
    immedServe = 0      #num customers served immediately
    custID = 0          #for immedServe and testing
    def __init__(self, env, calpha, cbeta, ialpha, ibeta):
        self.stock = simpy.Resource(env, capacity = 1)
        self.custa = calpha
        self.custb = cbeta
        self.inva = ialpha
        self.invb = ibeta
        self.simStartTime = 0.0
        self.ID = customer.custID
        customer.custID += 1

    def Run(self, env):
        # simulates customer arrival + purchase item
        while 1:
            yield self.stock.request()  #attempt to purchase
            custArrive = random.gammavariate(self.custa, self.custb)
            customer.custID += 1        #keep track of num customers in one sim
            yield env.timeout(custArrive)
            if(self.stock):
                customer.immedServe += 1
                #if we have available stock, no need to wait

            customer.waitTime += env.now - self.simStartTime   
            #otherwise, update wait time

    def restock(self, env):
        # simulate item arrival
        while 1:
            invArrive = random.gammavariate(self.inva, self.invb)
            yield env.timeout(invArrive)
            env.process(self.Run(env))
            #inventory restock.

def storesim(maxsimtime, alphac, betac, alphai, betai):
    env = simpy.Environment()
    C = customer(env, alphac, betac, alphai, betai)  #sim set up
    env.process(C.Run(env))
    env.run(until=maxsimtime)

    print C.waitTime / C.custID, C.immedServe / C.custID


#http://simpy.readthedocs.io/en/latest/topical_guides/porting_from_simpy2.html
#for working with simpy 3 
