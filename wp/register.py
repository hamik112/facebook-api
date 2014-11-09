import mechanize

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from facebook.utils.tools import save_res
#from facebook.utils.captcha_solver import CaptchaSolver
from facebook.utils.personal_data import personal_data

from random import choice
import StringIO
from PIL import Image
from bs4 import BeautifulSoup
import os
import urllib
import traceback
import json
from timeout_decorator import timeout

solver = False

def set_captcha_solver(csolver=False):
    global solver
    if solver and (not csolver):
        return None
    if not csolver:
        solver = CaptchaSolver()
    else:
        solver = csolver


#pertantak44349  http://1.hidemyass.com/ip-2/encoded/czovL3Byb2ZpbC53cC5wbC9yZWplc3RyYWNqYS5odG1sP3RpY2FpZD0xMTMxZmU%3D'))

@timeout(300)
def register(email=None, password=None, name=None, surname=None, male=None, age=None, captcha_solver=False, proxy=None):
    #set_captcha_solver(captcha_solver)
    br=mechanize.Browser()
    br.addheaders= [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')]
    br.set_handle_robots(False)
    br.set_proxies(proxy)
    save_res(br.open('https://profil.wp.pl/rejestracja.html'))
    return fill_in_form(br, email, password, name, surname, male, age)

def fill_in_form(br, email=None, password=None, name=None, surname=None, male=None, age=None):
    email, password, name, surname, male, age = personal_data(email, password, name, surname, male, age, extra=1, login_checker=check_login)
    img_link = BeautifulSoup(br.response().read()).select('.captcha img')[0]['src']
    print img_link
    #if 'encoded' in img_link:
    #    print img_link
    #    img_link = 'http'+urllib.unquote(img_link.split('/')[-1].replace('_','/')).decode('base64')
    #    print img_link
    im = Image.open(StringIO.StringIO(br.open_novisit(img_link).read()))
    im.save('cap.png')
    os.startfile('cap.png')
    captcha_res = raw_input('Cap:').strip()
    print captcha_res
    fields = {'login':email,
              'newPassword1':password,
              'newPassword2':password,
              'imie':name,
              'nazwisko':surname,
              'plec': [str(int(male))],
              'rokUrodzin': str(age[0]),
              'miesiacUrodzin': str(age[1]),
              'dzienUrodzin': str(age[2]),
              'accountType': ['1'],
              'wielkoscMiejscowosci':[str(choice(range(5)))],
              'wyksztalcenie':[str(choice(range(5)))],
              'zawod': [str(choice(range(10)))],
              'slowo': captcha_res
              }
    for n2 in range(10):
        br.select_form(nr=n2)
        try:
            br['slowo']
            break
        except:
            pass
    else:
        raise RegistrationFailed('Could not find a form!')
    print br.form
    for k,v in fields.iteritems():
        print k, v
        br[k] = v
    res = br.submit().read()
    save_res(res)
    if 'dobrze' in res:
        print 'Registered!'
        br.open(BeautifulSoup(res).select('a.sbm')[0]['href'])
        br.open(BeautifulSoup(br.response().read()).select('.thanks a')[0]['href'])
        return dict(zip(['email','password','name','surname','male','age'],
                        [email+'@wp.pl', password, name, surname, male, age]))
    else:
        try:
            mes = BeautifulSoup(res).select('#notification_adaptiveMergedInterrupts')[0].text.strip()
        except:
            mes = ''
            print traceback.format_exc()
        raise RegistrationFailed('Registration failed! '+mes)

def check_login(login):
        print 'Cand login:', login
        r =  json.loads(urllib.urlopen('https://profil.wp.pl/login_available.json?login=%s&name=&surname=&year='%login).read())['available']
        print 'Login available:', r
        return r

    

 
class RegistrationFailed(Exception):
    pass
    
