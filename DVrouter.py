import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads
import copy


class DVrouter(Router):
    """Distance vector routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """TODO: add your own class fields and initialization code here"""
        Router.__init__(self, addr)  # initialize superclass - don't remove
        self.heartbeatTime = heartbeatTime
        self.last_time = 0
        self.DEST={}
        self.Inf=16
        # Hints: initialize local state
        

    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        if packet.isTraceroute():
            try:
                self.send(self.DEST[packet.dstAddr]["Port"],packet)
            except:
                return
            # Hints: this is a normal data packet
            # if the forwarding table contains packet.dstAddr
            #   send packet based on forwarding table, e.g., self.send(port, packet)
            
        else:
            # Hints: this is a routing packet generated by your routing protocol
            # if the received distance vector is different
            #   update the local copy of the distance vector
            #   update the distance vector of this router
            #   update the forwarding table
            #   broadcast the distance vector of this router to neighbors

            Old=copy.deepcopy(self.DEST)

            Cont=loads(packet.content)

            for key,_ in Cont.items():
                
                if key==self.addr:
                    continue
                
                if Cont[key]["Cost"]>=self.Inf and self.DEST[key]["Nexthop"]==packet.srcAddr:
                    self.DEST[key]={}
                    self.DEST[key]['Cost']= self.Inf
                    self.DEST[key]['Port']= None
                    self.DEST[key]['Nexthop']=None
                    self.DEST[key]['IsN']=False
                    
                if key not in self.DEST.keys():
                    self.DEST[key]={}
                    self.DEST[key]['Cost']= self.DEST[packet.srcAddr]["Cost"]+Cont[key]["Cost"]
                    self.DEST[key]['Port']= self.DEST[packet.srcAddr]["Port"]
                    self.DEST[key]['Nexthop']=packet.srcAddr
                    self.DEST[key]['IsN']=False

                elif self.DEST[key]['Cost'] > self.DEST[packet.srcAddr]["Cost"]+Cont[key]["Cost"]:
                    self.DEST[key]={}
                    self.DEST[key]['Cost']= self.DEST[packet.srcAddr]["Cost"]+Cont[key]["Cost"]
                    self.DEST[key]['Port']= self.DEST[packet.srcAddr]["Port"]
                    self.DEST[key]['Nexthop']=packet.srcAddr
                    self.DEST[key]['IsN']=False



            if self.DEST!=Old:
                Content=dumps(self.DEST)
            
                for k,_ in self.DEST.items():
                    if self.DEST[k]['IsN']==True:
                        Pack=Packet(Packet.ROUTING,self.addr,self.DEST[k],Content)
                        self.send(self.DEST[k]['Port'],Pack)


    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # update the distance vector of this router
        # update the forwarding table
        # broadcast the distance vector of this router to neighbors

        if endpoint in self.DEST.keys() and cost > self.DEST[endpoint]["Cost"]:
            return

        self.DEST[endpoint]={}
        self.DEST[endpoint]['Cost']=cost
        self.DEST[endpoint]['Port']=port
        self.DEST[endpoint]['Nexthop']=endpoint
        self.DEST[endpoint]['IsN']=True

        Content=dumps(self.DEST)
        
        for key,_ in self.DEST.items():
            if self.DEST[key]['IsN']==True:
                Pack=Packet(Packet.ROUTING,self.addr,self.DEST[key],Content)
                self.send(self.DEST[key]['Port'],Pack)


    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        # update the distance vector of this router
        # update the forwarding table
        # broadcast the distance vector of this router to neighbors

        for key,_ in self.DEST.items():
            if self.DEST[key]['Port']==port:
                Link=key
                break
        
        self.DEST[Link]['Cost']=self.Inf
        self.DEST[Link]['Port']= None
        self.DEST[Link]['Nexthop']= None
        self.DEST[Link]['IsN']=False

        for key,_ in self.DEST.items():
            if self.DEST[key]['Nexthop']==Link:
                self.DEST[key]['Cost']=self.Inf
                self.DEST[key]['Port']= None
                self.DEST[key]['Nexthop']= None
                self.DEST[key]['IsN']=False
        
        Content=dumps(self.DEST)
        
        for key,_ in self.DEST.items():
            if self.DEST[key]['IsN']==True:    
                Pack=Packet(Packet.ROUTING,self.addr,self.DEST[key],Content)
                self.send(self.DEST[key]['Port'],Pack)
        
        


    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.last_time >= self.heartbeatTime:

            Content=dumps(self.DEST)
        
            for key,_ in self.DEST.items():
                if self.DEST[key]['IsN']==True:
                    Pack=Packet(Packet.ROUTING,self.addr,self.DEST[key],Content)
                    self.send(self.DEST[key]['Port'],Pack)
            
            self.last_time = timeMillisecs
            # broadcast the distance vector of this router to neighbors
            


    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return dumps(self.DEST)
        
        # return ""
