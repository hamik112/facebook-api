from bs4 import BeautifulSoup, NavigableString
import urllib

def get_proxies(n=1):
        raw_proxies = []
        for page in xrange(n):
            res = urllib.urlopen('https://hidemyass.com/proxy-list/%d'%(page+1))
            proxy_sr = BeautifulSoup(res.read(), "lxml")
            raw_proxies+=proxy_sr.select('tr')
        proxies = []
        for raw_proxy in raw_proxies:
            if raw_proxy.select('.slow'):
                continue
            try:
                ip  = extract_ip(raw_proxy)
            except:
                print 'Could not extract the IP'
                continue
            temp = raw_proxy.select('td')
            port = temp[2].text.strip()
            Type = temp[6].text.strip().lower()
            #print Type, ip, port
            if 'socks' in Type:
                continue
            proxies.append({Type:':'.join([ip, port])})
        return proxies

def extract_ip(raw_proxy):
        m=raw_proxy.select('td')[1]
        ch=list(list(m.children)[0].children)
        forbidden = []
        for style in ch[0].text.split():
            if 'none' in style:
                forbidden.append(style[1:style.index('{')])
        res = ''
        for c in ch[1:]:
            if type(c)==NavigableString:
                res+=str(c)
                continue
            if c.select('span'):
                res+=c.select('span')[0].text.strip()
                print res
                continue # not sure...
            try:
                if c['class'][0] in forbidden:
                    continue
            except:
                pass
            try:
                if 'none' in c['style']:
                    continue
            except:
                pass
            res+=c.text.strip()
        return res



    
