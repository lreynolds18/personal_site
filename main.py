import webapp2
import os
import jinja2
import urllib
import logging
import sys

import files
files = files.Files()

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
        
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
       	self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class Main(Handler):
    def get(self):
    	status = False
    	if urllib.urlopen("http://lucas-reynolds.appspot.com").getcode() == 200:
    		status = True
        self.render("main.html", status=status)
        
class Contact(Handler):
	def get(self):
		self.render("info.html")

class About(Handler):
	def get(self):
		para = """I am currently in my second year at Michigan State University.  I have been majoring in Computer Science.
				  I also have taken around three years of a second language: French. And for the programming languages that I am comfortable
				  with are Python and C++.  I've been using a lot of Python 2.7 in web development endeavors and on a raspberry pi.
				  I'm apart of the Solar Car Team so we use the raspberry pi as a back-up camera and a data collector.  I also have been creating
				  a server or media center with my own raspberry pi.  And I've been missing around with different Linux operating systems particularly Debian (Raspbian), 
				  Arch_Linux, and Ubuntu."""
		self.render("about.html", para=para)
	
class Projects(Handler):
	def get(self):
		projects =  {"python" : ["proj05.py", "proj06.py", "proj07.py", "proj08.py", "proj09-app.py", "proj09-test.py", 
				    "proj10-app.py", "proj10-test.py", "proj11.py", "currency.py"],
					"c++" : ["job.cpp", "job.h", "scheduler.cpp", "scheduler.h", "functions.cpp", "functions.h",
			        "market.cpp", "player.cpp",	"market.h", "player.h", "rand_walk.cpp", "rand_walk.h", 
			        "madlib.cpp", "madlib.h", "proj04.cpp"]}
		self.render("project.html", projects=projects)
		
class Project_Links(Handler):
	def render_page(self, file_content="", project_name=""):
		error = None
		if not file_content or file_content == "":
			error = "File could not be found."
		self.render("project_link.html", file_content=file_content, project_name=project_name, error=error)
		
	def get(self, project_name):
		p = {"proj05.py": files.proj05(), "proj06.py": files.proj06(), "proj07.py": files.proj07(), "proj08.py": files.proj08(),
			 "proj09-app.py": files.proj09app(), "proj09-test.py": files.proj09test(), "proj10-app.py": files.proj10app(), 
			 "proj10-test.py": files.proj10test(), "proj11.py": files.proj11(), "currency.py": files.currency(), 
			 "job.cpp": files.jobc(), "job.h": files.jobh(), "scheduler.cpp": files.schedulerc(), 
			 "scheduler.h": files.schedulerh(), "functions.cpp": files.functionsc(), "functions.h": files.functionsh(),
			 "market.cpp": files.marketc(), "player.cpp": files.playerc(), "market.h": files.marketh(), "player.h": files.playerh(),
			 "rand_walk.cpp": files.rand_walkc(), "rand_walk.h": files.rand_walkh(), "madlib.cpp": files.madlibc(), 
			 "madlib.h": files.madlibh(), "proj04.cpp": files.proj04c()}
		try:
			file = p[project_name]
		except:
			file = ""
			pass
		self.render_page(file_content=file, project_name=project_name)
			
app = webapp2.WSGIApplication([('/', Main),
							   ('/contact', Contact),
							   ('/about', About), 
							   ('/projects', Projects),
							   ('/projects/', Projects),
							   ('/projects/([--z]+)', Project_Links)],
						     debug=True)
