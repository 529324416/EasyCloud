import os

DIR = 0
FILE = 1

KB = 1024
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB

def typeList():

    return {
        "68746D6C3E": 'html',
        "d0cf11e0a1b11ae10000":'xls',
        "44656C69766572792D64":'eml',
        'ffd8ffe000104a464946':'jpg',
        '89504e470d0a1a0a0000':'png',
        '47494638396126026f01':'gif',
        '49492a00227105008037':'tif',
        '424d228c010000000000':'bmp',
        '424d8240090000000000':'bmp',
        '424d8e1b030000000000':'bmp',
        '41433130313500000000':'dwg',
        '3c21444f435459504520':'html',
        '3c21646f637479706520':'htm',
        '48544d4c207b0d0a0942':'css',
        '696b2e71623d696b2e71':'js',
        '7b5c727466315c616e73':'rtf',
        '38425053000100000000':'psd',
        '46726f6d3a203d3f6762':'eml',
        'd0cf11e0a1b11ae10000':'doc',
        'd0cf11e0a1b11ae10000':'vsd',
        '5374616E64617264204A':'mdb',
        '252150532D41646F6265':'ps',
        '255044462d312e350d0a':'pdf',
        '2e524d46000000120001':'rmvb',
        '464c5601050000000900':'flv',
        '00000020667479706d70':'mp4',
        '49443303000000002176':'mp3',
        '000001ba210001000180':'mpg',
        '3026b2758e66cf11a6d9':'wmv',
        '52494646e27807005741':'wav',
        '52494646d07d60074156':'avi',
        '4d546864000000060001':'mid',
        '504b0304140000080044':'zip',
        '504b03040a0000080000':'zip',
        '504b03040a0000000000':'zip',
        '526172211a0700cf9073':'rar',
        '235468697320636f6e66':'ini',
        '504b03040a0000000000':'jar',
        '4d5a9000030000000400':'exe',
        '3c25402070616765206c':'jsp',
        '4d616e69666573742d56':'mf',
        '3c3f786d6c2076657273':'xml',
        '494e5345525420494e54':'sql',
        '7061636b616765207765':'java',
        '406563686f206f66660d':'bat',
        '1f8b0800000000000000':'gz',
        '6c6f67346a2e726f6f74':'properties',
        'cafebabe0000002e0041':'class',
        '49545346030000006000':'chm',
        '04000000010000001300':'mxp',
        '504b0304140006000800':'docx',
        'd0cf11e0a1b11ae10000':'wps',
        '6431303a637265617465':'torrent',
        }
 
def bytes2hex(bytes):

    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()

# 获取文件类型
def filetype(filename):
    # print('读文件二进制码中……');
    binfile = open(filename, 'rb') # 必需二制字读取
    # print('提取关键码……');
    bins = binfile.read(20) #提取20个字符
    binfile.close() #关闭文件流
    bins = bytes2hex(bins) #转码
    bins = bins.lower()#小写
    tl = typeList()  #文件类型
    ftype = 'unknown'
    # print('关键码比对中……');
    for hcode in tl.keys():
        lens = len(hcode) # 需要的长度
        if bins[0:lens] == hcode:
            ftype = tl[hcode]
            break
    if ftype == 'unknown':#全码未找到，优化处理，码表取5位验证
        bins = bins[0:5];
        for hcode in tl.keys():
            if len(hcode) > 5 and bins == hcode[0:5]:
                ftype = tl[hcode]
                break
    return ftype

def fileobj(name,_type,size,filepath):

    return {
        "_type":FILE,
        "filename":name,
        "filepath":filepath,
        "filetype":_type,
        "filesize":size
    }

def folderobj(name,path):

    return {
        "_type":DIR,
        "dirname":name,
        "dirpath":path
    }

def file_size(filepath):
    '''get file size'''

    size =  os.path.getsize(filepath)
    if size < KB:
        return str(size) + "B"
    elif size < MB:
        return str(round(size/KB,2)) + "KB"
    elif size < GB:
        return str(round(size/MB,2)) + "MB"
    elif size < TB:
        return str(round(size/GB,2)) + "GB"
    else:
        return str(round(size/TB,2)) + "TB"


def scan_floder_first(floder):
    '''遍历一个文件夹下第一层目录的子文件和子目录'''

    _Ret = []
    for _sub in os.listdir(floder):
        _tmp = floder + _sub
        if os.path.isfile(_tmp):
            _filetype = filetype(_tmp)
            _filesize = file_size(_tmp)
            _filepath = _tmp
            _filename = _sub
            _Ret.append(fileobj(_filename,_filetype,_filesize,_filepath))
        else:
            _Ret.append(folderobj(_sub,_tmp))
    return _Ret

        
def delete_folder(dirpath):
    '''remove dir and all files in dirpath'''

    for file in os.listdir(dirpath):
        _target_file = dirpath + "/" + file
        if os.path.isdir(_target_file):
            delete_folder(_target_file)
        else:
            os.remove(_target_file)
    os.removedirs(dirpath)


if __name__ == '__main__':

    for file in scan_floder_first("./Files/"):
        print(file)