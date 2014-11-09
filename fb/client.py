import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from facebook.utils.tools import save_res
#from facebook.utils.captcha_solver import CaptchaSolver
from facebook.utils.wproxy import WProxy
from facebook.utils.wproxy import get_ips

from fexc import *
from browser import Browser
import re
import traceback
import urllib, json, urllib2
#from hmaproxylist import get_proxies
from timeout_decorator import timeout
from facebook.utils.accdb import AccDB

class FbClient:
    _mainurl = 'https://m.facebook.com'
    _encoding = "Windows-1250"
    
    def __init__(self, email='janebrownen@gmail.com', password='Thisis@test', proxy=None, ignore_errors=False):
        self.ignore_errors = ignore_errors
        if isinstance(email, dict):
            email, password, proxy = email['email'], email['password'], email['proxy']
        self.br = Browser()
        self.br.set_mianurl(self._mainurl)
        self.br.set_handle_robots(False)
        self.br.addheaders= [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0')]
        if proxy:
            if isinstance(proxy, dict):
                self.br.set_proxies(proxy)
            else:
                self.br.set_wproxy(proxy)
        self._login(email, password)

    @timeout(30)
    def _login(self, login, password):
        try:
            self.br.get(self._mainurl)
        except urllib2.HTTPError:
            raise Exception('Could not open login page!')
        print 'Works!'
        try:
            self.br.select_form_by_control_names(['email','pass'], ['year'])
        except NoUniqueForm:
            raise Exception('Could not find the login form!')
        self.br['email'], self.br['pass'] = login, password
        try:
            res = self.br.submit().read()
        except urllib2.HTTPError:
            raise Exception('Could not post login form!')
        try:
            self.br.select_form_by_control_names(['email','pass'], ['year'])
            save_res(self.br)
            raise ValueError('Invalid email or password! OR account banned.')
        except NoUniqueForm:
            pass
        if self.ignore_errors:
            return None
        try:
            save_res(self.br)
            self.br.select_form_by_control_names(['status', 'target'])
        except:
            raise AccessDenied('Has login verificaction! Can\'t bypass.')

    def valid_encoding(self, text, encoding=None):
        return text.decode(encoding if encoding else self._encoding).encode('utf-8')

    def post_status(self, text, targets = [], at=None, encoding=None):
        self.br.get(self._mainurl)
        self.br.select_form_by_control_names(['status', 'target'])
        self.br['status'] = self.valid_encoding(text, encoding)
        targets = valid_targets(targets)
        if at:
            if not at.isdigit():
                at = get_id(at, 'user')['id']
            self.br.form.new_control('text','at',{'value': at})
        self.br.form.new_control('text','users_with',{'value': ','.join(targets)})
        self.br.form.fixup()
        self.br.submit()

    def post_chat(self, text, targets):
        targets = ','.join(valid_targets(targets))
        chat_link = '/messages/compose/?folder=inbox&ids[%s]=%s'%(targets, targets)
        self.br.get(chat_link)
        self.br.select_form_by_control_names(['body'])
        self.br['body'] = self.valid_encoding(text)
        self.br.submit()

    def __like_page(self, link):
        '''works for pages only'''
        try:
            self.br.get(link)
            self.__post_like(self.br._find_link(['/a/profile.php?', 'fan', 'id'], ['comment']))
        except urllib2.HTTPError:
            raise AccessDenied('Could not open the page!')

    def like(self, link):
        '''works for pages, photos and posts!'''
        if '/posts/' in link or 'photo.php' in link:
            self.__like(link)
        else:
            self.__like_page(link)
     
    def __like(self, link):
        '''works for posts and photos'''
        try:
            self.br.get(link)
        except IndexError, urllib2.HTTPError:
            raise AccessDenied('Photo has to be public!')
        try:
            link = self.br._find_link(['like.php', 'perm'], ['comment'])
        except ValueError:
            raise  AccessDenied('Set your followers comment setting to public!')
        self.__post_like(link)

    def __post_like(self, link):
        decoded = self.br._wproxy.decode_url(link)
        print 'Decoded like url', decoded
        if 'ft_ent_identifier' in decoded or 'profile.php?' in decoded:
            if 'ul&perm' in decoded or 'profile.php?unfan' in decoded:
                print 'Already liked!'
            else:
                self.br.get(link)
        else:
            raise AccessDenied('Set your followers comment setting to public!')
        
    def comment(self, link, text):
        try:
            self.br.get(link)
        except urllib2.HTTPError:
            raise AccessDenied('Post has to be public!')
        try:
            self.br.select_form_by_control_names(['comment_text'])
        except NoUniqueForm:
            raise AccessDenied('Set your followers comment setting to public!')
        self.br['comment_text'] = self.valid_encoding(text)
        self.br.submit()

    def add_friend(self, target):
        self.br.get(str(target))
        self.br.get(self.br._find_link(['friends', '_add_friend']))

    
    def accept_friends(self, targets=False):
        '''Accepts all the friend requests from people on targets list (ids or link names).
          Accepts all friend requests if targets are set to false.'''
        #Make this function more redundant
        targets = valid_targets(targets) if targets else targets
        done = []
        acc = []
        while True:
            added = False
            self.br.get('friends/center/requests/')
            for req in self.br.select('.ib'):
                a_link = req.select('.btnC')[0]['href']
                cand = re.findall('confirm=\d+',a_link)[0].replace('confirm=','')
                if cand in done:
                    continue
                done.append(cand)
                if (not targets) or cand in targets:
                    #We have to add him!
                    self.br.get(a_link)
                    added = True
                    acc.append(cand)
            if not added:
                break
        print 'Added', acc

    def change_avatar(self, path):
        '''changes avatar of the account to the picture in path (file-like obj or path)'''
        if type(path)==str:
            path = open(path, 'rb')
        elif not hasattr(path, 'read'):
            raise ValueError('Path has to be a full path or file like object with read attr.')
        self.br.get('photos/change/profile_picture/?source=edit_profile&amp')
        self.br.select_form_by_control_names(['charset_test'])
        self.br.form.add_file(path, 'form-data', 'fb_dtsg')
        self.br.submit()
        
    def _click(self, bs):
        return self.br.get(bs['href'])



def valid_targets(targets):
    if type(targets)==str:
        targets = [targets]
    def repair(t):
        if target.isdigit():
            return target
        elif type(target)==int:
            return str(target)
        return get_id(target, 'user')['id']
    return [repair(target) for target in targets]


def get_id(s, typ):
    if typ=='user':
        return json.loads(urllib.urlopen('http://graph.facebook.com/'+s).read())
    else:
        raise ValueError('Invalid type!')
    
def register_account():
    pass
    


if __name__=='__main__':
    data  = {'password': 'Tongue&foot1', 'email': 'laumarek18@wp.pl', 'proxy': None}
    res = FbClient(data, ignore_errors=True)


