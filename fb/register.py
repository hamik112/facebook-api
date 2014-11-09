import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from facebook.utils.tools import save_res
#from facebook.utils.captcha_solver import CaptchaSolver
from facebook.utils.wproxy import WProxy, get_ips
from facebook.wp.register import register as mail_register
from facebook.wp.register import check_login as check_mail_availability
from facebook.wp.mail import get_secret_code
from facebook.utils.personal_data import personal_data
from client import FbClient
import datetime

from browser import Browser
import traceback
import time
import random
from timeout_decorator import timeout
#import cute_ip_changer
import string
FB_PASS = string.ascii_lowercase+string.digits+string.ascii_uppercase
if 0:
    cute_ip_changer.change_ip()

@timeout(600)
def register_account(encoding="Windows-1250", proxy=None):
    global br, data
    email, password, name, surname, male, age = personal_data(extra=0, login_checker=check_mail_availability)
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders= [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')]
    br.set_wproxy(proxy)
    br.get('r.php')
    fields = {'firstname': name.decode(encoding).encode('utf-8'),
              'lastname': surname.decode(encoding).encode('utf-8'),
              'email': email+'@wp.pl',
              'gender': [str(int(male+1))],
              'year': str(age[0]),
              'month': str(age[1]),
              'day': str(age[2]),
              'pass': password
              }
    br.select_form_by_control_names(fields.keys())
    print fields
    for k,v in fields.iteritems():
        print k, v
        try:
            br[k] = v
        except TypeError:
            print 'Strange:', k, v
            br[k] = [v]
        time.sleep(10)
    br.submit()
    
    try:
        br.select_form_by_control_names(['c'])
    except: #registration failed OR other verifications
        try:
            br.select_form_by_control_names(['day','month'])
            print 'Something went wrong. Check if you can register again?'
        except: # Other verifications ...
            print 'We have lost our info :('
        return br, 0
    save_res(br)
    while True:
        try:
            data  = mail_register(email, password, name, surname, male, datetime.datetime(*age))
            data['proxy'] = proxy
            break
        except:
            print traceback.format_exc()
    time.sleep(5)
    data['complete'] = False
    return complete_register(data, br)


def complete_register(data, br=None, last=False):
    try:
        br.select_form_by_control_names(['charset_test'],['c'])
        br.submit()
        print 'Resent email!'
    except: #Probably has to relogin
        print 'Could not find a resend form, logging again'
        br = FbClient(data, ignore_errors=True).br
        try:
            br.open(br._find_link(['phone', 's=1'])) # we dont want to have a phone :D
        except:
            print('Could not postpone phone number verification')
        br.select_form_by_control_names(['charset_test'],['c'])
        br.submit()
    try:
        br.select_form_by_control_names(['charset_test', 'c'])
        print 'Selected confirm code form'
    except:
        print 'Could not find confirm code form'
        if not last:
            print 'Retrying...'
            return complete_register(data, last=True)
        else:
            print 'Could not complete the registration! You will have to do that manually :('
            return br, data
    time.sleep(5)
    while True:
        try:
            code = get_secret_code(data)
            br['c'] = code
            print code
            br.submit()
            time.sleep(1)
            try:
                br.select_form_by_control_names(['c'])
                print 'Damn, the code was wrong!' # resend the email?
                time.sleep(10)
            except:
                break
        except:
            time.sleep(5)
            print traceback.format_exc()
    markers = ['step', 'skip']
    skipped = True
    while skipped:
        skipped = False
        for e in br.select('a'):
            try:
                if all([i in br._wproxy.decode_url(e['href']) for i in markers]):
                    skipped = True
                    print 'Skipped!'
                    br.get(e['href'])
                    time.sleep(1+random.randrange(3))
                    break
            except:
                pass
    print 'Success!!!!!!'
    print 'Your login:', data['email']
    print 'Your password', data['password']
    data['complete'] = True
    return br, data
    


