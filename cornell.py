import requests
from bs4 import BeautifulSoup as BS
import re
import urllib.request, urllib.parse, urllib.error  #url handling modules
import json
from fixture_builder import FixtureBuilder
from config_content_builder import ConfigBuilder

class Cornell:
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
		for title in soup.find_all("div", class_="views-field views-field-title"):
			course_title.append(''.join(title.findAll(text=True)))
			course_title.append(' \n')	
		
		self.new_list.append(course_title)
		return course_title

	def get_course_name_continue(self,soup_cont):
		course_title = []
		for title in soup_cont.find_all("div", class_="views-field views-field-title"):
			course_title.append(''.join(title.findAll(text=True)))
			course_title.append(' \n')	
		
		self.new_list.append(course_title)
		return course_title

	def get_image(self, soup):
		# Get the images of a specified course.
		course_image = []
		for link in soup.select('span.field-content img[src]'):
			course_image.append(link['src'])
			course_image.append(' \n')			
		self.new_list.append(course_image)
		
		return course_image

	def get_image_continue(self, soup_cont):
		course_image = []
		for link in soup_cont.select('span.field-content img[src]'):
			course_image.append(link['src'])
			course_image.append(' \n')			
		self.new_list.append(course_image)
		
		return course_image

	def get_course_description(self,soup):
		course_description = []
		for text in soup.find_all("div", class_="views-field views-field-field-short-description"):
			course_description.append(''.join(text.findAll(text=True)))
			course_description.append(' \n')	
		
		self.new_list.append(course_description)
		return course_description

	def get_course_description_continue(self,soup_cont):
		course_description = []
		for text in soup_cont.find_all("div", class_="views-field views-field-field-short-description"):
			course_description.append(''.join(text.findAll(text=True)))
			course_description.append(' \n')	
		
		self.new_list.append(course_description)
		return course_description

	def get_organization(self, soup):
		
		#Get the subjects of a specified course.
		organization = []
		for subject in soup.find_all("div", class_="views-field views-field-field-school-organization", ):
			organization.append(''.join(subject.findAll(text=True)))
			organization.append(' \n')
		self.new_list.append(organization)
		
		return organization			

	def get_organization_continue(self, soup_cont):
		
		#Get the subjects of a specified course.
		organization = []
		for subject in soup_cont.find_all("div", class_="views-field views-field-field-school-organization", ):
			organization.append(''.join(subject.findAll(text=True)))
			organization.append(' \n')
		self.new_list.append(organization)
		
		return organization					
	def get_course_page_urls(self,soup):
		"""
		Scrape Upenn "View All Courses" page for links to all courses.
		Returns: List of links to all courses.
		"""
		course_links =[]
		root_url = 'http://onlinelearning.cornell.edu'
		for link in soup.select('span.field-content a[href]'):
			new_url = root_url + link['href']
			course_links.append(new_url)
			course_links.append(' \n')
		
		self.new_list.append(course_links)
		return course_links
	
	def get_course_page_urls_continue(self,soup_cont):
		course_links =[]
		root_url = 'http://onlinelearning.cornell.edu'
		for link in soup_cont.select('span.field-content a[href]'):
			new_url = root_url + link['href']
			course_links.append(new_url)
			course_links.append(' \n')
		
		self.new_list.append(course_links)
		return course_links

	def run_all(self):
		view_courses_url = 'http://onlinelearning.cornell.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid'
		view_courses_url_cont = 'http://onlinelearning.cornell.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid&page=1'
		response = requests.get(view_courses_url)
		response_cont = requests.get(view_courses_url_cont)
		soup = BS(response.content, "html.parser")
		soup_cont = BS(response_cont.content, "html.parser")

		self.get_course_name(soup)
		self.get_course_name_continue(soup_cont)
		self.get_course_page_urls(soup)
		self.get_course_page_urls_continue(soup_cont)
		self.get_organization(soup)
		self.get_organization_continue(soup_cont)
		self.get_image(soup)
		self.get_image_continue(soup_cont)
		self.get_course_description(soup)
		self.get_course_description_continue(soup_cont)

	
		print (self.new_list)
		with open('cornell.txt', 'w+') as wr: # w+: create if file doesnt exist
			for course_doc in self.new_list:
				for name in course_doc:	
					wr.write(name)

	def json_convert(self):
		view_courses_url = 'http://onlinelearning.cornell.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid'
		view_courses_url_cont = 'http://onlinelearning.cornell.edu/welcome?f%5B0%5D=field_cost%3A98&view-order=grid&page=1'
		response = requests.get(view_courses_url)
		response_cont = requests.get(view_courses_url_cont)
		soup = BS(response.content, "html.parser")
		soup_cont = BS(response_cont.content, "html.parser")

		new_dict = zip(self.get_course_name(soup),
		#self.get_course_name_continue(soup_cont),
		self.get_course_page_urls(soup),
		#self.get_course_page_urls_continue(soup_cont),
		self.get_organization(soup),
		#self.get_organization_continue(soup_cont),
		self.get_image(soup),
		#self.get_image_continue(soup_cont),
		self.get_course_description(soup))
		#self.get_course_description_continue(soup_cont))

		new_dict = list(new_dict)
		keys = ['content_title', 'copyright_img_link', 'course_Organization', 'course_urls','course_Description']
		Cornell_course_list = []
		Cornell_course = {}
		
		for i in new_dict[::2]:
			i = list(i)
			mix_list = zip(keys,i)
			mix_list = list(mix_list)
			Cornell_course_list.append(dict(mix_list))
		Cornell_course["attribution"] = Cornell_course_list
		
		with open('cornell_resources.json', 'w+') as wr: 
			wr.write(json.dumps(Cornell_course))

if __name__ == '__main__':
	Cornell().json_convert()
	#Cornell().run_all()
