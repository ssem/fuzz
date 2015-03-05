import socket

class Scan:
    def __init__(self, ip, verbose):
        self.ip = ip
        self.verbose = verbose

    def tcp(self, start=1, stop=1000):
        if callable(self.verbose):
            self.verbose('starting tcp scan')
        for port in xrange(start, stop):
            if callable(self.verbose):
                percent = round(float(port-start)/float(stop-start)*100,1)
                if percent % 5 == 0:
                    self.verbose('TCP scan: {}%'.format(percent))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.ip, port))
            sock.close()
            if result == 0:
                yield port

    def udp(self, start=1, stop=1000):
        if callable(self.verbose):
            self.verbose('starting udp scan')
        for port in xrange(start, stop):
            if callable(self.verbose):
                percent = round(float(port-start)/float(stop-start)*100,1)
                if percent % 5 == 0:
                    self.verbose('UDP scan: {}%'.format(percent))
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            try:
                sock.sendto('', (self.ip, port))
                x = sock.recv(1)
            except socket.timeout:
                sock.close()
                continue
            sock.close()
            yield port

