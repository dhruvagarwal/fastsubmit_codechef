import mechanize, time, os, sys

def func(site):
	path=raw_input('Give your file path along with name and extension : ')
	fil=open(path).read()
	br.open('http://www.'+site+'.com/submit/'+raw_input("Enter Question Code : "))
	br.select_form(nr=0)
	br.form["body" if site=='codechef' else "file"]=fil
	br.submit()

def get_input(site):
	name = raw_input("Enter Username: ")
	password = raw_input("Enter Password: ")
	br.form["name" if site=='codechef' else "login_user"] = name
	br.form["name" if site=='codechef' else "login_user"] = password
	print "Please wait while we log you in..."
	br.submit()
	with open('credentials.txt', 'w') as credentials:
		credentials.write("%s\n" %site)
		credentials.write("%s\n" %name)
		credentials.write("%s" %password)

	
br=mechanize.Browser(factory=mechanize.RobustFactory())
br.set_handle_robots(False)
site=raw_input("Enter site's name (codechef/spoj) : ").lower()
if site in ['codechef','spoj']:
	br.open('http://www.'+site+'.com')
	br.select_form(nr=0)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	path = r"./"
	try:
		with open('credentials.txt', 'r') as credentials:
			fi = "credentials.txt"
			f = os.path.join(path, fi)
			data = credentials.read().split()
			if os.stat(f).st_mtime < time.time() - 2*60*60 or data[0] != site:
				os.remove(os.path.join(path, f))
				get_input(site)
			else:
				print "Please wait while we log you in..."
				br.form["name" if site=='codechef' else "login_user"] = data[1]
				br.form["name" if site=='codechef' else "login_user"] = data[2]

	except IOError as err:
		get_input(site)

	ch='y'
	while ch=='y':
		func(site)
		ch=raw_input("do you want to continue(y/n) : ")

	