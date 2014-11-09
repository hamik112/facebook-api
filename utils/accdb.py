import os
import time
import cPickle

DIR_PATH = os.path.dirname(__file__)

class AccDB:
    def __init__(self, path='accsdb.cpi'):
        if isinstance(path, file):
            path = path.name
            f = path
        elif isinstance(path, unicode) or isinstance(path, str):
            if '/' in path or '\\' in path:
                pass
            else:
                path = os.path.join(DIR_PATH, path)
            try:
                f = open(path, 'rb')
            except:
                with open(path, 'wb') as f:
                    cPickle.dump([], f)
                f = open(path, 'rb')      
        else:
            raise ValueError('Invalid path type!')
        try:
            self.data = cPickle.load(f)
        except:
            raise Exception('The file seems to be damaged!')
        self.path = path
        f.close()

    def __getitem__(self, i):
        return self.data[i]

    def __iter__(self):
        return iter(self.data)

    def add_account(self, info):
        req = ['email', 'password', 'proxy']
        if not all([e in info for e in req]):
            raise ValueError('Account info misses at least required key. '+str(req))
        if self.get('email', info['email']):
            return None
        info['creation_time'] = time.time()
        self.data.append(info)
        self.save()
        self.backup()

    def save(self):
        with open(self.path, 'wb') as f:
            cPickle.dump(self.data, f)

    def get(self, key, value):
        return [e for e in self.data if e.get(key)==value]

    def backup(self):
        with open(self.path+'.bak', 'wb') as f:
            cPickle.dump(self.data, f)

    def __str__(self):
        return ('Database contains %d accounts.\n'%len(self.data)+
                '\n'.join(sorted(['%s   %s'%(e['email'], e['password']) for e in self.data])))

    def __repr__(self):
        return self.__str__()
    
        
        
        
            
        
