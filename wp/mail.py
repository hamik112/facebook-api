# -*- coding: utf-8 -*-
import poplib
from bs4 import BeautifulSoup
import quopri
import re


def get_secret_code(account_data, serwer_pop='pop3.wp.pl' ):
    pop = poplib.POP3_SSL(serwer_pop)
    pop.user(account_data['email'])
    pop.pass_(account_data['password'])

    iloscW, zajeteMiejsce = pop.stat()
    
    for i in xrange(1,iloscW+1):
        mail = pop.retr(i)
        content = quopri.decodestring('\n'.join(mail[1]))
        markers = ['facebook']
        if not all([marker in content for marker in markers]):
            continue
        
        cand = [e.text.strip() for e in BeautifulSoup(content).select('span.expl strong')]
        if len(cand)==1 and len(cand[0])==5:
            pop.quit()
            return cand[0]
        cand = re.findall('code=\d\d\d\d\d&email', content)
        if not cand:
            continue
        print cand
        cand2 = filter(lambda x: x.isdigit(), cand[0])
        print cand2
        if len(cand2)==5:
            pop.quit()
            return cand2
    pop.quit()
    raise Exception('Could not find a code!')


        
        



