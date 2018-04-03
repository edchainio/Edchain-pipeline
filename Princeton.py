import requests
from bs4 import BeautifulSoup as BS
import re
import urllib.request, urllib.parse, urllib.error  #url handling modules
import json
from fixture_builder import FixtureBuilder
from config_content_builder import ConfigBuilder

class Princeton:
	# use vars and property decorator - convert to reader builder format
	def __init__(self):
        	self.content_download_urls = []
        	self.new_list = []

	def get_course_name(self,soup):
		"""
		Get the name of a specified course.
		Args: 
			soup - soupified homepage of course

		Returns: The course name.
		"""
		course_title = []
		for title in soup.find_all('td', {'class': 'views-field views-field-title'}):
			course_title.append(''.join(title.findAll(text=True)))

		self.new_list.append(course_title)
		return course_title

	def get_image(self, soup):
		#Get the images of a specified course.
		course_image = []
		for link in soup.findAll('td', {"class": "views-field views-field-field-page-image"}):
			course_image.append(link.img['src'])
			course_image.append(' \n')	
		self.new_list.append(course_image)
		return course_image

	def get_instructors(self, soup):
		"""
		Get the names of instructors of a specified course.
		Args:
			course_info_div - "html division" (container with course info)
		"""
		instructor_name = []
		for name in soup.find_all("td", class_="views-field views-field-field-instructor"):
			instructor_name.append(''.join(name.findAll(text=True)))		
		self.new_list.append(instructor_name)
		
		return instructor_name
	# def get_organization(self, soup):
		
	# 	#Get the subjects of a specified course.
	# 	organization = []
	# 	for subject in soup.find_all("div", class_="views-field views-field-field-school-organization", ):
	# 		organization.append(''.join(subject.findAll(text=True)))
	# 		organization.append(' \n')
	# 	self.new_list.append(organization)
		
	# 	return organization			

	# def get_organization_continue(self, soup_cont):
		
	# 	#Get the subjects of a specified course.
	# 	organization = []
	# 	for subject in soup_cont.find_all("div", class_="views-field views-field-field-school-organization", ):
	# 		organization.append(''.join(subject.findAll(text=True)))
	# 		organization.append(' \n')
	# 	self.new_list.append(organization)
		
	# 	return organization					
	def get_course_page_urls(self,soup):
		"""
		Scrape Princeton "View All Courses" page for links to all courses.
		Returns: List of links to all courses.
		"""
		course_links =[]
		root_url = 'http://onlinelearning.Princeton.edu'
		for link in soup.findAll('td', attrs={'class' : 'views-field views-field-title'}):
			new_url = root_url + link.find('a')['href']
			course_links.append(new_url)
			course_links.append(' \n')
		
		self.new_list.append(course_links)
		return course_links
	
	def run_all(self):
		view_courses_url = 'https://online.princeton.edu/courses'
		response = requests.get(view_courses_url)
		soup = BS(response.content, "html.parser")
        
		self.get_course_name(soup)
		self.get_course_page_urls(soup)
		self.get_instructors(soup)
		self.get_image(soup)
		


	
		print (self.new_list)
		with open('Princeton.txt', 'w+') as wr: # w+: create if file doesnt exist
			for course_doc in self.new_list:
				for name in course_doc:	
					wr.write(name)

	# def json_convert(self):
	# 	view_courses_url = 'http://onlinelearning.Princeton.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid'
	# 	view_courses_url_cont = 'http://onlinelearning.Princeton.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid&page=1'
	# 	response = requests.get(view_courses_url)
	# 	response_cont = requests.get(view_courses_url_cont)
	# 	soup = BS(response.content, "html.parser")
	# 	soup_cont = BS(response_cont.content, "html.parser")

	# 	new_dict = zip(self.get_course_name(soup),
	# 	#self.get_course_name_continue(soup_cont),
	# 	self.get_course_page_urls(soup),
	# 	#self.get_course_page_urls_continue(soup_cont),
	# 	self.get_organization(soup),
	# 	#self.get_organization_continue(soup_cont),
	# 	self.get_image(soup),
	# 	#self.get_image_continue(soup_cont),
	# 	self.get_course_description(soup))
	# 	#self.get_course_description_continue(soup_cont))

	# 	new_dict = list(new_dict)
	# 	keys = ['content_title', 'course_urls', 'course_Organization', 'copyright_img_link','course_Description']
	# 	Princeton_course_list = []
	# 	Princeton_course = {}
		
	# 	for i in new_dict[::2]:
	# 		i = list(i)
	# 		mix_list = list(zip(keys,i))
	# 		print (mix_list)
	# 		Princeton_course_list.append(dict(mix_list))
	# 	Princeton_course["attribution"] = Princeton_course_list

	# 	# with open('Princeton_resources.json', 'w+') as wr: 
	# 	# 	wr.write(json.dumps(Princeton_course))

if __name__ == '__main__':
    Princeton().run_all()
