import requests
from bs4 import BeautifulSoup as BS
import re
import urllib.request, urllib.parse, urllib.error  #url handling modules
import json
from fixture_builder import FixtureBuilder
from config_content_builder import ConfigBuilder

class Yale:
	# use vars and property decorator - convert to reader builder format

	def __init__(self):
		self.content_download_urls = []
		self.new_list = []

	def get_course_name(self,soup):
		course_title = []
		for title in soup.find_all("td", class_="views-field views-field-title-1"):
			course_title.append(''.join(title.findAll(text=True)))	
		
		self.new_list.append(course_title)
		return course_title
        
	def get_course_department(self,soup):
		course_department = []
		for text in soup.find_all("td", class_="views-field views-field-title active"):
			course_department.append(''.join(text.findAll(text=True)))
			course_department.append(' \n')	
	
		self.new_list.append(course_department)
		return course_department

	def get_course_number(self, soup):
		
		#Get the subjects of a specified course.
		course_number = []
		for subject in soup.find_all("td", class_="views-field views-field-field-course-number", ):
			course_number.append(''.join(subject.findAll(text=True)))
        
		
		self.new_list.append(course_number)
		
		return course_number
        
	def get_instructor_name(self, soup):
		"""
		Get the names of instructors of a specified course.
		Args:
			course_info_div - "html division" (container with course info)
		"""
		instructor_name = []
		for name in soup.find_all("td", class_="views-field views-field-field-professors-last-name"):
			instructor_name.append(''.join(name.findAll(text=True)))		
		self.new_list.append(instructor_name)
		return instructor_name

	def get_course_date(self,soup):
		course_date =[]
		for date in soup.find_all("td", class_="views-field views-field-field-semester"):
		    course_date.append(''.join(date.findAll(text=True)))
		    course_date.append(' \n')
		
		self.new_list.append(course_date)
		return course_date

	def get_course_page_urls(self,soup):
		"""
		Scrape Upenn "View All Courses" page for links to all courses.
		Returns: List of links to all courses.
		"""
		course_links =[]
		root_url = 'http://onlinelearning.Yale.edu'
		for link in soup.select('span.field-content a[href]'):
			new_url = root_url + link['href']
			course_links.append(new_url)
			course_links.append(' \n')
		
		self.new_list.append(course_links)
		return course_links

	def run_all(self):
		view_courses_url = 'https://oyc.yale.edu/courses'
		response = requests.get(view_courses_url)
		soup = BS(response.content, "html.parser")

		self.get_course_name(soup)
		self.get_course_number(soup)
		# self.get_course_page_urls(soup)
		self.get_instructor_name(soup)
		self.get_course_date(soup)
		# self.get_image(soup)
        # self.get_course_description(soup)


	
		with open('Yale.txt', 'w+') as wr: # w+: create if file doesnt exist
			for course_doc in self.new_list:
				for name in course_doc:	
					wr.write(name)

	def json_convert(self):
		view_courses_url = 'http://onlinelearning.Yale.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid'
		view_courses_url_cont = 'http://onlinelearning.Yale.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid&page=1'
		response = requests.get(view_courses_url)
		response_cont = requests.get(view_courses_url_cont)
		soup = BS(response.content, "html.parser")
		soup_cont = BS(response_cont.content, "html.parser")

		new_dict = zip(self.get_course_name(soup),
		#self.get_course_name_continue(soup_cont),
		self.get_course_page_urls(soup),
		self.get_course_number(soup))

		new_dict = list(new_dict)
		keys = ['content_title', 'course_urls', 'course_Organization', 'copyright_img_link','course_Description']
		Yale_course_list = []
		Yale_course = {}
		
		for i in new_dict[::2]:
			i = list(i)
			mix_list = list(zip(keys,i))
			print (mix_list)
			Yale_course_list.append(dict(mix_list))
		Yale_course["attribution"] = Yale_course_list

		# with open('Yale_resources.json', 'w+') as wr: 
		# 	wr.write(json.dumps(Yale_course))

if __name__ == '__main__':
	Yale().run_all()
	#Yale().run_all()
