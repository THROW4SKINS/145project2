from SimPy.Simulation import *
from random import seed
# Two discrete events are running at the same time
# inventory = Resource(1) modeled the number of items in inventory
# DES(Inventory) is used to simulate the deliveries of new inventory
# DES(customer) is used to simulate the arrival and purchase of customer

class G:  # globals
   # inventory = Resource(0)
   stock = Level()
   alphac = 0.0
   betac = 0.0
   alphai = 0.0
   betai =0.0

class Inventory(Process):
    addTime = 0.0
    totInv = 0
    def Run(self):
        # simulate item arrival
        while 1:
            # print G.stock.amount
            TBA = random.gammavariate(G.alphai, G.betai)
            yield hold, self, TBA
            yield put,self,G.stock,1
            Inventory.totInv += 1
            Inventory.addTime = now()
            # print Inventory.addTime

            # print G.stock.amount




class customer(Process):
    # simulates customer arrival and service
    # sorry for misleading name OO is hard and
    # so is simpy

    waitTime = 0.0  # total wait time for all customers
    immedServe = 0  # num customers served immediately
    custID = 0  # for immedServe and testing

    def Run(self):
        # simulates customer arrival + purchase item
            t1 = 0.0
            customer.custID += 1
            if (G.stock.amount >= 1):
                customer.immedServe += 1
                yield get, self, G.stock, 1
            else:
                t1 = now()                # print now()
                yield get,self,G.stock,1  # attempt to purchase
                customer.waitTime += Inventory.addTime - t1




class Source(Process):
    """ Source generates customers regularly """

    def generate(self):
        while 1:
            TBA = random.gammavariate(G.alphac, G.betac)
            yield hold, self, TBA
            c = customer()
            activate(c, c.Run())

                    ## Model/Experiment ------------------------------
def storesim(maxsimtime, alphac, betac, alphai, betai):
    seed(12345)
    G.alphac = alphac
    G.betac = betac
    G.alphai = alphai
    G.betai = betai
    initialize()
    s = Source()
    c= customer()
    i = Inventory()
    activate(s, s.generate())
    activate(i, i.Run())
    # activate(c, c.Run())
    simulate(until=maxsimtime)
    m = float(customer.waitTime) / customer.custID
    imm = float(customer.immedServe)/customer.custID
    tot = float(customer.immedServe)/Inventory.totInv
    # print 'total number of order:', customer.custID
    # print 'total waiting time: ', customer.waitTime
    # print 'number of order filled up immediately: ',customer.immedServe
    # print 'mean wait time: ', (m)
    # print 'proportion of orders served immediately', (imm)
    return (m,imm,tot)



i = storesim(10000,2,2.2,2,2)
print i
