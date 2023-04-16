from mininet.topo import Topo
from mininet.link import TCLink

class ATopo(Topo):
    def __init__(self, hosts, loss):
        # Initialize topology
        Topo.__init__(self)

        if hosts < 2:
            print("Cantidad invalida de hosts!")
            exit(1)

        if loss < 0:
            print("El porcentaje de perdidas no puede ser negativo")
            exit(1)

        clients = hosts - 1
        created_clients = 0

        # Create hosts
        h1 = self.addHost('Servidor')
        while(created_clients < clients):
            c = self.addHost('cliente_' + str(created_clients + 1))
            self.addLink(h1, c, cls=TCLink, loss=loss)
            created_clients += 1


topos = {'customTopo': ATopo}