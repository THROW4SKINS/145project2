from SimPy.Simulation import *
from random import seed
# Two discrete events are running at the same time
# inventory = Resource(1) modeled the number of items in inventory
# DES(stock) is used to simulate the deliveries of new inventory
# DES(customer) is used to simulate the arrival and purchase of customer

class G:  # globals
   inventory = Resource(1)

class stock(Process):
    def __init__(self):
        Process.__init__(self)

    def Run(self,a,b):
        # simulate item arrival
        while 1:
            invArrive = random.gammavariate(a, b)
            yield hold, self, invArrive
            yield request, self, G.inventory
            G.inventory.n += 1
            yield release, self, G.inventory


class customer(Process):
    # simulates customer arrival and service
    # sorry for misleading name OO is hard and
    # so is simpy

    waitTime = 0.0  # total wait time for all customers
    immedServe = 0  # num customers served immediately
    custID = 0  # for immedServe and testing

    def __init__(self):
        Process.__init__(self)
        self.simStartTime = 0.0
        self.ID = customer.custID
        customer.custID += 1


    def Run(self,a,b):
        # simulates customer arrival + purchase item
        while 1:
            if (G.inventory.n > 0):
                customer.immedServe += 1
                # if we have available stock, no need to wait
            yield request,self,G.inventory  # attempt to purchase
            G.inventory.n -= 1              # purchase finished, decrease inventory
            custArrive = random.gammavariate(a,b) # inter-arrival time for next customer
            customer.custID += 1  # keep track of num customers in one sim

            yield hold,self,custArrive

            customer.waitTime += now() - self.simStartTime
            yield release,self,G.inventory

#
# class Source(Process):
#     def generate(self, number, a,b):
#         for i in range(number):
#             C = customer()
#             activate(C, C.Run(a,b))
#             t = random.gammavariate(a, b)
#             yield hold, self, t
#
#
# ## Experiment data -------------------------
#
# maxNumber = 1


## Model/Experiment ------------------------------
def storesim(maxsimtime, alphac, betac, alphai, betai):
    seed(12345)
    initialize()
    C = customer()
    activate(C, C.Run(alphac,betac))
    I = stock()
    activate(I, I.Run(alphai,betai))
    simulate(until=maxsimtime)
    print (customer.waitTime / customer.custID)

storesim(10000,2,2.2,2,2)

