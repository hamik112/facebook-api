import cPickle
import urllib2
import os
from bs4 import BeautifulSoup
import re

PPATH = os.path.join(os.path.dirname(__file__), 'wproxies.cpi')
PROXIES = cPickle.load(open(PPATH, 'rb'))

def get_ips():
   return PROXIES.keys()

def open_hma(serv, ip):
   try:
       url = 'http://%d.hidemyass.com/ip-%d'
       req = urllib2.Request(url%(serv, ip))
       res = urllib2.urlopen(req, timeout=4).read()
       return BeautifulSoup(res,'lxml')
   except:
      return False

   
def update():
   form = 'http://%d.hidemyass.com/ip-%d/encoded/'
   res = {}
   b = open_hma(1,1)
   serv_lim = int(b.select('.server')[0].text.strip()[-1])
   for serv in xrange(serv_lim):
       b = b if not serv else open_hma(serv+1, 1)
       if not b:
           continue
       ip_lim = int(b.select('.ip')[0].text.strip()[-1])
       for ip in xrange(ip_lim):
           b = b if not ip else open_hma(serv+1, ip+1)
           if not b:
               continue
           cip = re.findall('(\d+\.\d+\.\d+\.\d+)', b.select('.current')[0].text)[0].strip('()')
           res[cip] =form%(serv+1,ip+1)
   global PROXIES
   PROXIES = res
   cPickle.dump(res, open(PPATH, 'wb'))
   return res



class WProxy:
    def __init__(self, ip=None):
        if ip:
            self.__ip = ip
            try:
                self.__base = PROXIES[ip]
                if not self.__base.endswith('/'):
                    self.__base+='/'
                    print 'Fixed base link'
            except KeyError:
                raise ValueError('IP not available!')
        else: # dont do anything!
            self.__class__ = Transparent

    def test(self, test_url='http://www.example.com/'):
        test_url = self.encode_url(test_url)
        try:
            req = urllib2.Request(test_url)
            #req.add_header('Referer', 'http://www.python.org/')
            resp = urllib2.urlopen(req, timeout=4)
            content = resp.read()
            return True
        except:
            return False

    def encode_url(self, url):
        assert url.startswith('http')
        url = url[4:]
        return self.__base + urllib2.quote(url.encode('base64').replace('/', '_').replace('\n',''))

    def decode_url(self, url):
        assert url.startswith(self.__base)
        url = url[len(self.__base):]
        return 'http'+urllib2.unquote(url).replace('_', '/').decode('base64')
        

class Transparent(WProxy):
    def encode_url(self, url):
        return url
    def decode_url(self, url):
        return url
    
