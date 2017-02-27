from SimPy.Simulation import *
from random import seed
# Two discrete events are running at the same time
# inventory = Resource(1) modeled the number of items in inventory
# DES(Inventory) is used to simulate the deliveries of new inventory
# DES(customer) is used to simulate the arrival and purchase of customer

class G:  # globals
   # inventory = Resource(0)
   stock = Level()

class Inventory(Process):

    def Run(self,a,b):
        # simulate item arrival
        while 1:
            invArrive = random.gammavariate(a, b)
            delivery = 1
            yield put,self,G.stock,delivery
            # print G.stock.amount
            yield hold, self, invArrive



class customer(Process):
    # simulates customer arrival and service
    # sorry for misleading name OO is hard and
    # so is simpy

    waitTime = 0.0  # total wait time for all customers
    immedServe = 0  # num customers served immediately
    custID = 0  # for immedServe and testing
    simStartTime = 0.0
    def __init__(self):
        Process.__init__(self)

        self.ID = customer.custID
        # customer.custID += 1


    def Run(self):
        # simulates customer arrival + purchase item
        while 1:
            customer.simStartTime = now()
            customer.custID += 1
            if (G.stock.amount >= 1):
                customer.immedServe += 1
                yield get, self, G.stock,1
            else:
                t1 = now()
                yield get,self,G.stock,1  # attempt to purchase
                customer.waitTime += now() - customer.simStartTime

class Source(Process):
    """ Source generates customers regularly """

    def generate(self, TBA):
            c = customer()
            activate(c, c.Run())
            yield hold, self, TBA

                    ## Model/Experiment ------------------------------
def storesim(maxsimtime, alphac, betac, alphai, betai):
    seed(12345)
    initialize()
    s = Source()
    ARRint = random.gammavariate(alphac, betac)
    activate(s, s.generate(TBA=ARRint))
    I = Inventory()
    activate(I, I.Run(alphai,betai))
    simulate(until=maxsimtime)
    print 'total order created:', customer.custID
    print 'total waiting time: ', customer.waitTime
    print 'number of order filled up immediately: ',customer.immedServe
    print 'mean wait time: ', (customer.waitTime / customer.custID)
    # print (float(customer.immedServe / customer.custID))

storesim(10000,2,2.2,2,2)

#result is wrong, I am trying to fix it
