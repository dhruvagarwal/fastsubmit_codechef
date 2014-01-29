import mechanize,urllib,os,time,thread,threading
from bs4 import BeautifulSoup

def get_input(site):
        name = raw_input("Enter Username: ")
        password = raw_input("Enter Password: ")
        br.form["name" if site=='codechef' else "login_user"] = name
        br.form["pass" if site=='codechef' else "password"] = password
        data=[site,name,password]
        print "Please wait while we log you in..."
        br.submit()
        with open('credentials.txt', 'w') as credentials:
                credentials.write("%s\n" %site)
                credentials.write("%s\n" %name)
                credentials.write("%s\n" %password)
        return data
        

def f_submit(site):
        path = raw_input('Give your file path along with name and extension : ')
        fil = open(path).read()
        br.open('http://www.'+site+'.com/submit/' + raw_input("Enter Question Code : "))
        br.select_form(nr=0)
        br.form["body" if site=='codechef' else "file"]=fil
        return br.submit()

def recheck_cc(solution_id):
        response = mechanize.urlopen('http://www.codechef.com/viewsolution/'+solution_id)
        parser = BeautifulSoup(str(response.read()))
        div_list = parser.find_all('div', class_='head')
        for divs in div_list:
                for content in divs.contents:
                        if str(content).find('Status') is not -1:
                                status = str(content).split(',')[0]
                                return status.split(':')[1]

def cc():
    	response = f_submit('codechef')
    	html_code = str(response.read())
    	html_code = html_code.split('\n')
    	for line in html_code:
    		if line.find('var submission_id') is not -1:
    			tokens = line.split()
    			solution_id = tokens[3].split(';')[0]
    			print "Running your solution"
    			res=recheck_cc(solution_id)
    			while '??' in res:
    				res=recheck_cc(solution_id)
    			print res

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
        f_submit('spoj')
        c=0
        res=recheck(user)
        print "Running your solution"
        while res=='??':
                res=recheck(user)
        print res
                       
br = mechanize.Browser()
br.set_handle_robots(False)
site = raw_input("Enter site's name (codechef/spoj) : ").lower()

if site in ['codechef','spoj']:
    	br.open('http://www.'+site+'.com')
    	br.select_form(nr=0)
    	path = "./"
    	try:
    		with open('credentials.txt', 'r') as credentials:
    			fi = "credentials.txt"
    			f = os.path.join(path, fi)
    			data = credentials.read().split()
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
    		cc() if site=='codechef' else sp(data[1])
    		ch=raw_input("do you want to continue(y/n) : ")
