import time
import hashlib


def md5(text):
    '''md5 encrypto'''

    _m = hashlib.md5()
    _m.update(text)
    return _m.hexdigest()


def get_global_code(salt="pwd"):
    ''' get time code'''

    _time = time.localtime()
    return "{}{}{}".format(_time[0],_time[1],_time[2]) + salt

def verify(pwd):

    if pwd == md5(get_global_code().encode()):
        return True
    return False


if __name__ == '__main__':

    print(md5(get_global_code().encode()))