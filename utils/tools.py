import datetime
from collections import defaultdict



def days_ago(n, pattern):
    '''returns a date n days ago in the given pattern
    eg: %Y-%m-%d  gives 2014-07-06'''
    return (datetime.datetime.now()-datetime.timedelta(days=n)).strftime(pattern)



def save_res(r):
    if hasattr(r, 'response'):
        r = r.response()
    if not type(r) in [str, unicode]:
        r=r.read()
    with open('r.html','wb') as f:
        f.write(r)
        
def lcs(x, y):
    s_x = len(x)
    s_y =  len(y)
    y_previous = s_x*[0]
    cx, cy = x.lower(), y.lower()
    k, up_value, x_end, max_len = 0, 0, 0, -1
    while k<s_y:
         n=0
         diagonal_value=0
         while n<s_x:
             up_value=y_previous[n]
             if cx[n]==cy[k]:
                 y_previous[n] = diagonal_value+1
                 if diagonal_value>max_len:
                     max_len = diagonal_value
                     x_end = n
             else:
                 y_previous[n] = 0       
             diagonal_value = up_value
             n+=1
         k+=1
    return x[x_end-max_len: x_end+1]

def closest_match(phrase, lis):
    asses = lambda phrase, cand: float(len(lcs(phrase, cand)))/min(len(phrase), len(cand))
    d = [asses(phrase, e) for e in lis]
    return lis[d.index(max(d))]
    
def universal_dict(d, date_pattern, variables, dc=['Date', 'Country']):
    correct_variables = ['Offers Made', 'Offers Accepted', 'Offers Installed', 'Approved Installs', 'Cost']
    for e in d:
        for v, cv in zip(variables, correct_variables):
            if (not v) or v==cv:
                continue
            e[cv] = e[v]
            del e[v]
        e[dc[0]] = to_tuple(e[dc[0]], date_pattern)
        country = e[dc[1]]
        if country in countries.countries:
            e[dc[1]] = country
        elif country in countries.rcountries:
            e[dc[1]] = countries.rcountries[country]
        elif len(country)<4:
            print 'Unknown country:', country
            e[dc[1]] = country
        else:
            match = closest_match(country, countries.countries.keys())
            print 'Could not find country:', country, 'Closest match:', match
            print
            e[dc[1]] = match
    return dict_list(d, dc)

def dict_list(big, key):
    '''Converts a list of dicts to a dict of dicts'''
    new = defaultdict(list)
    for small in big:
        val = small[key[0]]
        del small[key[0]]
        new[val].append(small)
    if len(key)!=1:
        for k in new:
            new[k] = dict_list(new[k], key[1:])
    return dict(new)
 
def to_datetime(obj, pattern=False):
    if type(obj) in (tuple, list): #univ tuple (year, month, day)
         return datetime.datetime(*tuple(obj)) 
    elif type(obj)==datetime.datetime:
        return obj
    elif type(obj) in (str, unicode):
        return to_datetime(to_tuple(obj, pattern))
    elif type(obj)==int:
        return datetime.datetime.now()-datetime.timedelta(days=obj)
    raise Exception('Unknown obj type!')
    
def to_tuple(s, pattern=False):
    if type(s) in [str, unicode]:
        s = replace_month_name(s)
        pattern = [e for e in filter(lambda x: x in 'Ymd%', pattern).split('%') if e]
        d = []
        res = 0
        for e in s+'&':
            if e.isdigit():
                res = 10*int(res)+int(e)
            else:
                if res:
                    d.append(res)
                    res = 0
        r = dict(zip(pattern, d))
        return r['Y'] if r['Y']>1000 else r['Y']+2000, r['m'], r['d']
    elif type(s)==datetime.datetime:
        return s.year, s.month, s.day
    elif type(s)==int:
        return to_tuple(to_datetime(s))
    elif type(s) in [list, tuple]:
        return s
    raise Exception('Unknown obj type!')
    
    
def univ_date_handler(start, stop, pattern, inf=True, inl=False):
    '''Returns start and stop dates in the correct string pattern.
       inf if start is in the results
       inl if stop is in the results
       start and stop can be int, str( in the correct pattern), datetime or univ tuple (Year, Month, Day)
    '''
    stop = stop if stop else 0
    start = to_datetime(start, pattern)
    stop = to_datetime(stop, pattern)
    shift = datetime.timedelta(days=1)
    if not inf:
        start+= to_datetime(start, pattern)-shift
    if inl:
        stop+= -shift
    return start.strftime(pattern), stop.strftime(pattern)
    

def replace_month_name(s):
    months = 'January February March April May June July August September October November December'
    mup = months.split()
    mlo = months.lower().split()
    for typ in (mup, mlo):
        for n, name in enumerate(typ, 1):
            s = s.replace(name, str(n))
    return s
            
            
              
              

    
