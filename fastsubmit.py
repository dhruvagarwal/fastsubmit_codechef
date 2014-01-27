import mechanize

def f(site):
	path=raw_input('Give your file path along with name and extension : ')
	fil=open(path).read()
	br.open('http://www.'+site+'.com/submit/'+raw_input("Enter Question Code : "))
	br.select_form(nr=0)
	br.form["body" if site=='codechef' else "file"]=fil
	br.submit()
	
br=mechanize.Browser()
br.set_handle_robots(False)
site=raw_input("Enter site's name (codechef/spoj) : ").lower()
if site in ['codechef','spoj']:
	br.open('http://www.'+site+'.com')
	br.select_form(nr=0)
	br.form["name" if site=='codechef' else "login_user"]=raw_input("Enter handle/Username : ")
	br.form["pass" if site=='codechef' else "password"]=raw_input("Enter password : ")
	br.submit()
	ch='y'
	while ch=='y':
		f(site)
		ch=raw_input("do you want to continue(y/n) : ")

	
