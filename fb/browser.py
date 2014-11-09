import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from facebook.utils.wproxy import WProxy

import mechanize
from bs4 import BeautifulSoup
from fexc import NoUniqueForm


class Browser(mechanize.Browser):
    _mainurl = 'https://m.facebook.com'
    _wproxy = WProxy(None)
    
    def set_mianurl(self, url):
        self._mainurl = url

    def set_wproxy(self, wproxy):
        if isinstance(wproxy, WProxy):
            self._wproxy = wproxy
        elif isinstance(wproxy, dict):
            self.set_proxies(wproxy)
        else:
            self._wproxy = WProxy(wproxy)

    def _find_link(self, markers, nomarkers=[]):
        res = []
        for can in self.select('a'):
            raw = can['href']
            try:
                link = self._wproxy.decode_url(raw)
            except:
                continue
            if all([i in link for i in markers]) and all([not c in link for c in nomarkers]):
                res.append(raw)
        print 'Links found:', res
        if len(res)!=1:
            raise ValueError('No unique link!')
        return res[0]
        
    def get(self, url, data=None):
        if 'encoded' in url:
            url = self._wproxy.decode_url(url)
        if 'www.facebook.com' in url:
            url = url[url.index('www.facebook.com'):].replace('www.facebook.com', '')
        if not (self._mainurl in url or url.startswith('/')):
                url = '/'+url
        url = self._mainurl+url if url.startswith('/') else url
        print 'Prev',url
        print 'Real',self._wproxy.encode_url(url)
        
        return self.open(self._wproxy.encode_url(url), data)
    
    def select_form_by_control_names(self, names, no_names=[]):
        res = []
        for ind, f in enumerate(self.forms()):
            n = [e.name for e in f.controls]
            if not (all([name in n for name in names]) and all([not name in n for name in no_names])):
                continue
            res.append((f, ind))
        if len(res)!=1: 
            raise NoUniqueForm('No unique form with these control names!')
        self.select_form(nr=res[0][1])
        self.form.set_all_readonly(False)
        return res[0][0]

    def select(self, selector):
        return BeautifulSoup(self.response().read(), 'lxml').select(selector)



    
        
