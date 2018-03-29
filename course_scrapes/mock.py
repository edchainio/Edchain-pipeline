import requests
from bs4 import BeautifulSoup as BS
import re
import urllib.request, urllib.parse, urllib.error  #url handling modules

from fixture_builder import FixtureBuilder
from config_content_builder import ConfigBuilder
  
class Pennstate:
	# use vars and property decorator - convert to reader builder format

	def __init__(self):
		self.content_download_urls = []
		self.new_list = []

	def process(self):
		# get links to all course home pages
		course_page_urls = self.get_course_page_urls()

		# find courses licensed under Creative Commons, pass their
		# information to the builder for construction of product
		#self.get_allowed_course_page_urls(course_page_urls)

		# get product
		product = self.get_product()

		#content_urls = self.get_course_content()
	def get_course_name(self,soup):
		"""
		Get the name of a specified course.
		Args: 
			soup - soupified homepage of course

		Returns: The course name.
		"""
		course_title = []
		for title in soup.find_all("td", class_="column-1"):
			course_title.append(''.join(title.findAll(text=True)))
			#course_title.append(' \n')	
		for i in range(len(course_title)):
			course_title[i] = course_title[i].replace('\n' or '<br />', "")	
			#course_title.append(' \n')		
		#print (course_title)
		BigO = []
		for i in course_title:
			BigO.append(i)
			BigO.append(' \n')	

		self.new_list.append(BigO)
		return course_title													 
		
	def get_instructors(self, soup):
		"""
		Get the names of instructors of a specified course.

		Args:
			course_info_div - "html division" (container with course info)
		"""
		instructor_name = []
		for name in soup.find_all("td", class_="column-2"):
			instructor_name.append(''.join(name.findAll(text=True)))
			instructor_name.append(' \n')			
		self.new_list.append(instructor_name)
		
		return instructor_name

	def get_disciplines(self, soup):
		
		#Get the subjects of a specified course.
		discipline = []
		for subject in soup.find_all("td", class_="column-3"):
			discipline.append(''.join(subject.findAll(text=True)))
			course_title.append(' \n')	
		self.new_list.append(discipline)
		
		return discipline				
	def get_course_page_urls(self,soup):
		"""
		Scrape Upenn "View All Courses" page for links to all courses.
		Returns: List of links to all courses.
		"""
		
		course_links =[]
		for link in soup.select('td.column-1 a[href]'):
			course_links.append(link['href'])
			course_links.append(' \n')
		
		self.new_list.append(course_links)
		#print (course_links)
		return course_links
	
	def run_all(self):
		view_courses_url = 'https://www.onlinelearning.upenn.edu/courses/'
		response = requests.get(view_courses_url)
		soup = BS(response.content, "html.parser")

		self.get_course_name(soup)
		self.get_course_page_urls(soup)
		self.get_disciplines(soup)
		self.get_instructors(soup)

		with open('../ui/static/penn_state.txt', 'w+') as wr: # w+: create if file doesnt exist
			for course_doc in self.new_list:
				for name in course_doc:	
					wr.write(name)
				
		 # for _ in global_var:
		 # wr.write(self.get_course_name())
	

# def main():
# 	director = Pennstate(FixtureBuilder(), ConfigBuilder())
# 	director.construct()

if __name__ == '__main__':
	#Pennstate().get_course_page_urls(soup)
	Pennstate().run_all()
