import requests
import time
from bs4 import BeautifulSoup as BS
from pytube import YouTube, Playlist
import os
import pafy
import json
import pprint

class Yale_Video:
	def __init__(self):
		self.content_download_urls = []
	
	def get_course_title(self,soup):
		#Scrape playlist to get video playlist
		r = requests.get('https://www.youtube.com/playlist?list=PLh9mgdi4rNex7SOvB0Yhkkb-V_k2CkdcA')
		page = r.text
		soup=BS(page,'html.parser')
		end_url=soup.find_all('a',{'class':'pl-video-title-link'})
		title = []


		video_url=[]
		for course in end_url:
			root_url ='https://www.youtube.com'
			v = pafy.new(root_url + course.get("href"))
			video_url.append(v.title)
			title.append(v.title)
			video_url.append(root_url + course.get("href"))
		lecture_title = []
		lecture_link = []
		
		for idx,link in enumerate(video_url):
			if idx % 2 == 0:
				#start from index 3 which will eliminate initial digit title
				new_link = link[3:].strip()
				lecture_title.append(new_link)
			else:
				lecture_link.append(link)	

		#create list of courses numbered		
		lecture_index = list(range(0,len(lecture_title)))
		keys = ['id','lecture_title', 'lecture_url']
		
		course_dict = zip(lecture_index,lecture_title,lecture_link)
		course_dict = list(course_dict)

		Youtube_course = {}
		Yale_lecture_list = []

		for course_data in course_dict:
			i = list(course_data)
			mix_list = list(zip(keys,i))
			Yale_lecture_list.append(dict(mix_list))
			Youtube_course["youtube_content"] = Yale_lecture_list

		with open('Frontiers_Biomedical.json', 'w+') as wr: 
			wr.write(json.dumps(Youtube_course, indent=4))

		return video_url	
	def run_all(self):
		r = requests.get('https://www.youtube.com/playlist?list=PL27E877E8206F196B')
		page = r.text
		soup=BS(page,'html.parser')

		self.get_course_title(soup)

if __name__ == '__main__':
	Yale_Video().run_all()
