import mechanize,urllib,os,time,threading,thread,pickle,random, getpass
from bs4 import BeautifulSoup
import urllib2, sys

class mythread (threading.Thread):
	    def __init__(self,site,user):
	        threading.Thread.__init__(self)
	        self.site = site
	        self.user=user
	    def run(self):
	        threadLock.acquire()
	        cc() if self.site=='codechef' else sp(self.user)
	        threadLock.release()

def get_input(site):
        name = raw_input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")
        br.form["name" if site=='codechef' else "login_user"] = name
        br.form["pass" if site=='codechef' else "password"] = password
        data=[site,name,password]
        print "Please wait while we log you in..."
        br.submit()
        with open('credentials.txt', 'wb') as credentials:
                pickle.dump(data, credentials)
        return data

def ran_string(res, list):
    if res.strip() == 'AC':
            print random.choice(myList[0])
    elif res.strip() == 'TLE':
            print myList[1] 
    else:
    	try:
    		d=int(res.strip())
    	except:
    		print random.choice(myList[2])                   
def select_form(form):
	return form.attrs.get('id', None) == 'problem-submission'

def f_submit(site,langlist):
    path = raw_input('Give your file path along with name and extension: ')
    fil = open(path).read()
    question_code = raw_input("Enter Question Code: ")
    br.open('http://www.'+site+'.com/submit/' + question_code)
    #br.select_form(nr=0)
    br.select_form(predicate=select_form)
    br.form["program" if site=='codechef' else "file"]=fil
    print "Please choose the programming language(Enter the number corresponding to it):"
    i=1
    for lang in langlist:
    	for key in lang:
    		print("%d. %s" % (i,key))
    	i+=1
    sub = raw_input()
    key, value = (langlist[int(sub)-1]).popitem()
    br.form["language" if site=='codechef' else "lang"]=[value]
    return br.submit()

def recheck_cc(solution_id):
	site= 'http://www.codechef.com/viewsolution/'+solution_id
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(site,headers=hdr)
	response = urllib2.urlopen(req)
	parser = BeautifulSoup(str(response.read()))
	div_list = parser.findAll("div", { "class" : "head" })
	for divs in div_list:
	        for content in divs.contents:
	                if str(content).find('Status') is not -1:
	                        status = str(content).split(',')[0]
	                        final_status = status.split(': ')[1]
	                        return final_status
	return -1

def cc():
            response = f_submit('codechef',langlist)
            html_code = str(response.read())
            html_code = html_code.split('\n')
            for line in html_code:
                    if line.find('var submission_id') is not -1:
                            tokens = line.split()
                            solution_id = tokens[3].split(';')[0]
                            print "Running your solution. Sit tight."
                            res=recheck_cc(solution_id)
                            while True:
                            	if res == -1:
                                    res=recheck_cc(solution_id)
                                else:
                                    break
                            print res
                            ran_string(res, myList)

def recheck(user):
        c=0
        prob_list=mechanize.urlopen('http://www.spoj.com/status/'+user+'/signedlist').read().split('\n')
        for x in prob_list:
                x=x.replace('|',' ').split()
                if len(x)<8 or c<2:
                        if len(x)>7:
                                c+=1
                        continue
                else:
                        return x[4]

def sp(user):
        f_submit('spoj',langlist)
        c=0
        res=recheck(user)
        print "Running your solution. Sit tight."
        while res=='??':
                res=recheck(user)
        print res
        ran_string(res, myList)
        
myList = []
myList.append(['That was awesome!','Your IQ is off the charts!','Now that was some pretty cool stuff','You rock! Nice job.', 'Very NIce'])
myList.append(['You almost nailed that one! A little quicker next time.'])
myList.append(['That\'s sad. You should consider trying again','This is programming. You know that, right?','Aww, snap!', 'Oh, drat!'])
langlist = []
langlist.append({'C(gcc-4.8.1)':'11'})
langlist.append({'C++(gcc-4.3.2)':'41'})
langlist.append({'C++(gcc-4.9.2)':'1'})
langlist.append({'C++11(gcc-4.8.1)':'44'})
langlist.append({'C#(gmcs-2.0.1)':'27'})
langlist.append({'Java(javac-1.7.0_25)':'10'})
langlist.append({'Python(python-2.7.2)':'4'})
langlist.append({'Python3(python-3.1.2)':'116'})
threadLock = threading.Lock()                 
br = mechanize.Browser()
br.set_handle_robots(False)
site = raw_input("Enter site's name (codechef/spoj): ").lower()
if site in ['codechef','spoj']:
    br.open('http://www.'+site+'.com')
    br.select_form(nr=0)
    path = "./"
    try:
                    with open('credentials.txt', 'rb') as credentials:
                            fi = "credentials.txt"
                            f = os.path.join(path, fi)
                            data = pickle.load(credentials)
                            if os.stat(f).st_mtime < time.time() - 60*60 or data[0] != site: #change timeout here by default it's one hour (60*60)
                                    os.remove(os.path.join(path, f))
                                    get_input(site)
                            else:
                                    print "Please wait while we log you in..."
                                    try:
                                            br.form["name" if site=='codechef' else "login_user"] = data[1]
                                            br.form["pass" if site=='codechef' else "password"] = data[2]
                                            br.submit()
                                    except:
                                            data=get_input(site)
    except IOError as err:
        data=get_input(site)
    ch='y'
    
    while ch=='y':
                    if site=='codechef':
                    	t_cc=mythread(site,data[1])
                    	t_cc.start()
                    	t_cc.join()
                    else:
						t_sp=mythread(site,data[1])
						t_sp.start()
						t_sp.join()
                    ch=raw_input("Do you want to continue(y/n): ")
