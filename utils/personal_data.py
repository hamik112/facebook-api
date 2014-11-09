import random
import string
import datetime
import cPickle
import os.path

males=['Jakub', 'Jan', 'Mateusz', 'Bartek', 'Kacper', 'Szymon', 'Antoni', 'Filip', 'Piotr', 'Maciej', 'Aleksander', 'Adam', 'Wiktor', 'Krzysztof', 'Wojtek', 'Igor', 'Karol', 'Dawid', 'Tomasz', 'Patryk', 'Oskar', 'Dominik', 'Kamil', 'Oliwier', 'Ignacy', 'Marcel', 'Hubert', 'Adrian', 'Sebastian', 'Julian', 'Krystian', 'Marcin', 'Tymon']

females=['Julia', 'Maja', 'Zuzia', 'Aleksandra', 'Natalia', 'Wiktoria', 'Zofia', 'Oliwia', 'Maria', 'Alicja', 'Amelia', 'Lena', 'Gabriela', 'Karolina', 'Weronika', 'Martyna', 'Emilia', 'Patrycja', 'Marta', 'Nikola', 'Nina', 'Dominika', 'Helena', 'Agata', 'Laura', 'Kinga', 'Paulina', 'Klaudia', 'Michalina', 'Iga', 'Milena']

surnames=['Nowak', 'Kowalski', 'Lewandowski', 'Kowalczyk', 'Jankowski', 'Wojciechowski', 'Kwiatkowski', 'Kaczmarek', 'Mazur', 'Krawczyk', 'Piotrowski', 'Grabowski', 'Nowakowski', 'Michalski', 'Nowicki', 'Adamczyk', 'Dudek', 'Wieczorek', 'Majewski', 'Olszewski', 'Jaworski', 'Malinowski', 'Pawlak', 'Witkowski', 'Walczak', 'Rutkowski', 'Michalak', 'Sikora', 'Ostrowski', 'Baran', 'Duda', 'Szewczyk', 'Tomaszewski', 'Pietrzak', 'Marciniak', 'Zalewski', 'Jakubowski', 'Zawadzki', 'Sadowski', 'Chmielewski', 'Borkowski', 'Czarnecki', 'Sawicki', 'Kubiak', 'Maciejewski', 'Kucharski', 'Wilk', 'Kalinowski', 'Mazurek', 'Wysocki', 'Adamski', 'Wasilewski', 'Sobczak', 'Andrzejewski', 'Zakrzewski', 'Sikorski', 'Krajewski', 'Gajewski', 'Szymczak', 'Szulc', 'Baranowski', 'Laskowski', 'Makowski', 'Przybylski', 'Nowacki', 'Borowski', 'Chojnacki', 'Ciesielski', 'Szczepaniak', 'Krupa', 'Kaczmarczyk', 'Kowalewski', 'Urbaniak', 'Kozak', 'Kania', 'Czajkowski', 'Mucha', 'Tomczak', 'Markowski', 'Kowalik', 'Nawrocki', 'Brzozowski', 'Janik', 'Wawrzyniak', 'Markiewicz', 'Tomczyk', 'Jarosz', 'Kurek', 'Wolski', 'Dziedzic', 'Stasiak', 'Stankiewicz', 'Urban', 'Dobrowolski', 'Pawlik', 'Kruk', 'Piasecki', 'Wierzbicki', 'Polak', 'Janicki', 'Sosnowski', 'Bednarek', 'Majchrzak', 'Bielecki', 'Sowa', 'Milewski', 'Gajda', 'Klimek', 'Olejniczak', 'Ratajczak', 'Romanowski', 'Matuszewski', 'Madej', 'Kasprzak', 'Grzelak', 'Socha', 'Czajka', 'Marek', 'Kowal', 'Bednarczyk', 'Skiba', 'Wrona', 'Owczarek', 'Marcinkowski', 'Matusiak', 'Orzechowski', 'Sobolewski', 'Kurowski', 'Rogowski', 'Olejnik', 'Mazurkiewicz', 'Czech', 'Janiszewski', 'Bednarski', 'Chrzanowski', 'Bukowski', 'Czaja', 'Lisowski', 'Grzybowski', 'Pluta', 'Morawski', 'Sobczyk', 'Augustyniak', 'Rybak', 'Marzec', 'Konieczny', 'Marczak', 'Zych', 'Michalik', 'Kaczor', 'Kubicki', 'Paluch', 'Niemiec', 'Sroka', 'Stefaniak', 'Cybulski', 'Kacprzak', 'Kasprzyk', 'Kujawa', 'Lewicki', 'Przybysz', 'Stachowiak', 'Piekarski', 'Matysiak', 'Janowski', 'Murawski', 'Cichocki', 'Witek', 'Niewiadomski', 'Staniszewski', 'Bednarz', 'Lech', 'Rudnicki', 'Kulesza', 'Turek', 'Chmiel', 'Biernacki', 'Skrzypczak', 'Karczewski', 'Drozd', 'Pietrzyk', 'Komorowski', 'Antczak', 'Banach', 'Filipiak', 'Grochowski', 'Graczyk', 'Gruszka', 'Klimczak', 'Siwek', 'Konieczna', 'Serafin', 'Bieniek', 'Godlewski', 'Kulik', 'Zawada', 'Ptak', 'Strzelecki', 'Zarzycki', 'Mielczarek', 'Bartkowiak', 'Krawiec', 'Janiak', 'Bartczak', 'Winiarski', 'Tokarski', 'Panek', 'Konopka', 'Frankowski', 'Banasiak', 'Grzyb', 'Rakowski', 'Zaremba', 'Skowron', 'Dobosz', 'Witczak', 'Nawrot', 'Sienkiewicz', 'Kostrzewa', 'Kucharczyk', 'Rybicki', 'Biernat', 'Bogusz', 'Rogalski', 'Szymczyk', 'Janus', 'Szczepanik', 'Buczek', 'Szostak', 'Kaleta', 'Kaczorowski', 'Tkaczyk', 'Grzegorczyk', 'Drzewiecki', 'Trojanowski', 'Jurek', 'Gawron', 'Wojtczak', 'Rogala', 'Kula', 'Kubik', 'Maliszewski', 'Radomski', 'Kisiel', 'Cebula', 'Rosiak', 'Grzesiak', 'Gawlik', 'Cygan', 'Rojek', 'Bogucki', 'Mikulski', 'Walkowiak', 'Malec', 'Flis', 'Czapla', 'Drozdowski', 'Rzepka', 'Pawelec', 'Lipski', 'Wnuk', 'Andrzejczak', 'Zaborowski', 'Falkowski', 'Filipek', 'Ciszewski', 'Nowaczyk', 'Bielawski', 'Krysiak', 'Hajduk', 'Lisiecki', 'Mroczek', 'Pietras', 'Karwowski', 'Lach', 'Dziuba', 'Borek', 'Krakowiak', 'Wasiak', 'Skrzypek', 'Lasota', 'Mika', 'Juszczak', 'Borowiec', 'Sobieraj', 'Dubiel', 'Dominiak', 'Kmiecik', 'Bujak', 'Kubacki', 'Pilarski', 'Gutowski', 'Misiak', 'Tarnowski', 'Bartosik', 'Mierzejewski', 'Jakubiak', 'Twardowski', 'Zielonka', 'Jezierski', 'Jurkiewicz', 'Florczak', 'Janas', 'Bilski', 'Stelmach', 'Bochenek', 'Stec', 'Staszewski', 'Dudziak', 'Noga', 'Skoczylas', 'Pasternak', 'Matuszak', 'Piwowarczyk', 'Filipowicz', 'Milczarek', 'Adamus', 'Cholewa', 'Olczak', 'Koza', 'Czechowski', 'Wilczek', 'Kaczmarski', 'Jankowiak', 'Strzelczyk', 'Kubica', 'Misztal', 'Sieradzki', 'Adamczak', 'Szwed']

def make_female_surname(surname):
   if surname[-3:] in ['ski','zki','cki']:
      return surname[0:-1]+'a'
   return surname

def get_surname(male=True):
    if male:
       return random.choice(surnames)
    return make_female_surname(random.choice(surnames))


def get_name(male=True):
    if male:
        return random.choice(males)
    return random.choice(females)

def login_from_name(name, age, extra=3):
   name = filter(lambda x: x in string.printable, name)
   org=name
   name=name.split(' ')
   if len(name[0])<2 or len(name[1])<2:
      raise ValueError("Invalid name")
   login=''
   if 1:
      n_part=random.randrange(4)+1
      s_part=random.randrange(4)+1
      a=random.randrange(2)
      a_part=random.randrange(5)
      n_low=random.randrange(4)
      separation=random.randrange(4)
      if n_part!=4:
         login+=name[0][0:n_part]
      else:
         login+=name[0]
      if not n_low:
            login.lower()
      if not separation:
         login+=['1','2','3'][random.randrange(3)]
      if a and not a_part:
         login+=str(age)
      if s_part!=4:
         login+=name[1][0:s_part]
      else:
         login+=name[1]
      if a and a_part:
         login+=str(age)
   login = login.replace(' ','')
   if len(login)<7:
      return login_from_name(org, age, extra)
   return login+(random_nr(extra) if extra else '')


def random_nr(l=3):
   return str(random.randrange(10**(l-1),10**l))

def random_str(length, small_letter=1, upper_letter=1, digit=1, symbol=1, symbols = False):
   if symbol+upper_letter+digit+small_letter>length:
      raise ValueError('Cant satisfy your request! (Length to small)')
   small_letter += length-(symbol+upper_letter+digit+small_letter)
   vals = small_letter, upper_letter, digit, symbol
   syms = ['abcdefghijklmnoprstuwxyz',
           'ABCDEFGHIJKLMNOPRSTUWXYZ',
           '0123456789',
           '!@#&*()_+-=[]|:<>' if not symbols else symbols]
   char_list = [0]*vals[0]+[1]*vals[1]+[2]*vals[2]+[3]*vals[3]
   random.shuffle(char_list)
   return ''.join([random.choice(syms[e]) for e in char_list])



def cute_password(length, has_symbol=True, has_digit=False, connect=False, symbols=False, _data=[0]):
   '''Returns a nice password of a given length :) Dont use for length<8 or length>13 '''
   has_symbol = int(bool(has_symbol))
   has_digit = int(bool(has_digit))
   if length>13:
      raise ValueError('Max len is 13. (password would not be random enough otherwise)')
   if length<4+has_symbol+has_digit:
      raise ValueError('Password too short. Recommended 12 or more! To 100% avoid this error set 6 or more.')
   if not _data[0]:
      _data[0] = cPickle.load(open(os.path.join(os.path.dirname(__file__), 'words.cpi'),'rb'))
   symbols = '!#-_&$' if not symbols else symbols
   digs = '1579'
   if length>7+has_symbol+has_digit and (random.randrange(3) or connect):
      L1 = random.randrange(4, length-3-has_symbol-has_digit)
      L2 = length - L1 - has_digit - has_symbol
      W1 = random.choice(_data[0][L1])
      W2 = random.choice(_data[0][L2])
      if random.randrange(2) and not connect:
         base = W1.title()+W2.title()
         if has_symbol:
            base+= random.choice(symbols)
         if has_digit:
            base+= random.choice(digs)
      else:
         if has_symbol:
            base = W1.title()+random.choice(symbols)+W2
            if has_digit:
               base+= random.choice(digs)
         elif has_digit:
            base = W1.title()+random.choice(digs)+W2
         else:
            base = W1+W2.title()
   else:
      base = random.choice(_data[0][length-(has_symbol+has_digit)]).title()
      if has_digit:
         base+=random.choice(digs)
      if has_symbol:
         base+= random.choice(symbols)
   return base

      
      
      
   
      
def personal_data(email=None, password=None, name=None, surname=None, male=None, age=None, extra=3, login_checker=lambda x: True):
    male = bool(male if male is not None else random.randrange(2))
    if not type(age)==datetime.datetime:
        age = random.randrange(18, 40) if not age else age
        now = datetime.datetime.now()
        age = datetime.datetime(now.year-age,now.month, now.day)-datetime.timedelta(days=random.randrange(40,364))
    name = name if name else get_name(male)
    surname =  surname if surname else get_surname(male)
    while not email:
       email = login_from_name(name+' '+surname, age.day, extra)
       email = email if login_checker(email) else False
    password = cute_password(12, has_symbol=True, has_digit=True) if not password else password
    return [email.lower(), password, name, surname, male, (age.year, age.month, age.day)]
    
   

def get_address():
    raise NotImplemented

def get_city():
   raise NotImplemented

def get_country():
   raise NotImplemented

def get_street():
   raise NotImplemented

def get_postcode():
   raise NotImplemented
   
