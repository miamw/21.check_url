import sys
import urllib2
from urllib2 import Request, urlopen

SEP = '\t'
CON = ':'

#function: parse one label
def parse(str):
    str.replace('<br>', CON)
    while str.find('<') != -1:
        str2 = str[0:str.find('<')] + str[str.find('>')+1:]
        str = str2
    return str

#function: fetch data from one ip adress
def fetchIp(ip, browser):
    
    req = Request('http://whatismyipaddress.com/ip/'+ip, headers={'User-Agent' : browser})
    
    contents = ip
    try:
        response = urlopen(req)
        a = response.read()
        
        for label in configs:
            if a.find('<tr><th>'+label+'</th><td>') != -1:
                start = a.find('<tr><th>'+label+'</th><td>') + len(('<tr><th>'+label+'</th><td>'))
                end = a.find('</td>', start)
                contents += SEP + parse(a[start:end])
            else:
                contents += SEP + 'NULL'
    except urllib2.URLError:
        contents += SEP + 'Error'
    finally:
        return contents


config_file_path = 'label.config'

#parse input
if len(sys.argv) == 1:
    print '''\
Info: You are using the autofinder for whatismyipaddress.com
Usage:
        python autofinder.py [inputfile] ([outputfile]) ([-configfile])
        '''
    sys.exit(0)

elif len(sys.argv) >= 2:
    input_file_path = sys.argv[1]
    print 'Input File:'+input_file_path

    if len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[2].startswith('-')):
        output_file_path = input_file_path + '_out.txt'
    elif len(sys.argv) == 3:
        if sys.argv[2].startswith('-'):
            config_file_path = sys.argv[2][1:]
        else:
            output_file_path = sys.argv[2]
    elif len(sys.argv) == 4:
        output_file_path = sys.argv[2]
        if not sys.argv[3].startswith('-'):
            print 'Format Error: Config File path is not appropriatly typed(missed "-"?):' + sys.argv[3]
            sys.exit(0)
        else:
            config_file_path = sys.argv[3][1:]
    else:
        print '''\
Error: Too many parameters
Usage:
        python autofinder.py [inputfile] ([outputfile]) ([-configfile])
        '''
        sys.exit(0)

print 'Output File:'+output_file_path
print 'Config File:'+config_file_path

#parse config file. The item starts with '#' is not considered
config_file = open(config_file_path)
configs = []
for line in config_file:
    if not line.startswith('#'):
        configs.append(line[0:len(line)-1])

config_file.close()

#the file write mode is write
output_file = open(output_file_path, 'w')

browser_suffix = 'my brower'
cnt = 0
for line in open(input_file_path):
    # set and change the item 'User-Agent' of HTTP request cyclically to escape the TP filter of whatismyipaddress.com
    browser = '%d' %cnt + browser_suffix
    cnt = cnt+1
    
    ip = line[0:len(line)-1]
    ans = fetchIp(ip,browser)
    
    output_file.write(ans+'\n')
    print ans

    import time
    time.sleep(10)

output_file.close()
