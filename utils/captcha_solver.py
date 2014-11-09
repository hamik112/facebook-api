import deathbycaptcha as dbc
import traceback

class CaptchaSolver:
    ''' API to death by captcha. PAID :(

        To solve a captcha use solve method giving the path to the
        captcha image file (stored on your computer). After some
        time it should return the text that was in the captcha.
        If the text is not valid then use report_last method.

        Cheaper but much slower method is change_ip from cute_ip_changer (2 minutes)
    '''
    def __init__(self, login='piodrus', password='drukarka'):
        self.solver=dbc.HttpClient(login, password)

    def solve(self, path, timeout=60):
        try:
           self.last_captcha=self.solver.decode(open(path,'rb'),timeout)
        except:
            print traceback.format_exc()
            raise 
            return False
        if self.last_captcha:
            return self.last_captcha['text']
        return False

    def report_last(self):
        return self.solver.report(self.last_captcha['captcha'])
