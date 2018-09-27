#coding:gbk
import urllib2,urllib,cookielib,re
 
'''
 通用的登陆DZ论坛
 参数说明parms:
   username:用户名(必填),
   password :密码(必填),
   domain:网站域名，注意格式必须是：http://www.xxx.xx/(必填),
   answer:问题答案,
   questionid:问题ID,
   referer:跳转地址
    
 这里使用了可变关键字参数(相关信息可参考手册)
'''
def login_dz(**parms):
 
  #初始化
  parms_key = ['domain','answer','password','questionid','referer','username']
  arg = {}
  for key in parms_key:
    if key in parms:
      arg[key] = parms[key]
    else:
      arg[key] = ''
       
  #cookie设置
  cookieFile = './kan_cookies.dat'
  cookie = cookielib.LWPCookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
 
  #获取formhash
  pre_login = arg['domain']+'member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
  c = opener.open(pre_login).read()
  cookie.save(cookieFile)
  patt = re.compile(r'.*?name="formhash".*?value="(.*?)".*?')
  formhash = patt.search(c)
  if not formhash:
    raise Exception('GET formhash Fail!')
  formhash = formhash.group(1)
 
  #登陆
  postdata = {
   'answer':arg['answer'],
   'formhash':formhash,
   'password':arg['password'],
   'questionid':0 if arg['questionid']=='' else arg['questionid'],
   'referer':arg['domain'] if arg['referer']=='' else arg['referer'],
   'username':arg['username'],
    }
 
  postdata = urllib.urlencode(postdata)
  req = urllib2.Request(
    url= arg['domain']+'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LCaB3&inajax=1',
    data=postdata
    )
  c = opener.open(req).read(300)
  flag = '登陆失败 %s'%arg['username']
  if 'succeedhandle_login' in c:
    flag = True
  return flag
 
 
#使用例子：基本参数登陆
user='xxx'
pwd='xxx'
dom='http://www.discuz.net/' #另一个测试网站：http://bbs.jb51.net/
try:
  flag = login_dz(username=user,password=pwd,domain=dom)
  print(flag)
except Exception,e:
  print('Error:',e)