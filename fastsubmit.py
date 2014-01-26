import mechanize

def f():
	path=raw_input('Give your file path along with name and extension : ')
	fil=open(path).read()
	br.open('http://www.codechef.com/submit/'+raw_input("Enter Question	Code : "))
	br.select_form(nr=0)
	br.form["body"]=fil
	br.submit()
	
br=mechanize.Browser()
br.set_handle_robots(False)
br.open('http://www.codechef.com')
br.select_form(nr=0)
br.form["name"]=raw_input("Enter handle/Username : ")
br.form["pass"]=raw_input("Enter password : ")
br.submit()
ch='y'
while ch=='y':
	f()
	ch=raw_input("do you want to continue(y/n) : ")
