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
	
	def get_course_title(self,url1,soup):
		#Scrape playlist to get video playlist
		url = 'https://www.youtube.com'+url1
		print(url)
		r = requests.get(url)
		page = r.text
		soup=BS(page,'html.parser')
		end_url=soup.find_all('a',{'class':'pl-video-title-link'})
		title = []
		courseTitle = str(soup.title)

		courseTitle = courseTitle.replace("<title>","")
		courseTitle = courseTitle.replace("</title>","")
		
		youtube_course = {"title":courseTitle }
		count=0
		video_url=[]
		for course in end_url:
			root_url ='https://www.youtube.com'
			print("cccc",course.get("href"))
			v = pafy.new(root_url + course.get("href"))
			video_url.append(v.title)
			title.append(v.title)
			video_url.append(root_url + course.get("href"))
			count=count+1
			#remove if stmt
			# if count==3:
			# 	break

		#print('vurl',video_url)
		lecture_title = []
		lecture_link = []
		
		for idx,link in enumerate(video_url):
			if idx % 2 == 0:
				#start from index 3 which will eliminate initial digit title
				#new_link = link[3:].strip()
				lecture_title.append(link)
			else:
				lecture_link.append(link)	

		#create list of courses numbered		
		lecture_index = list(range(0,len(lecture_title)))
		keys = ['id','lecture_title', 'lecture_url']
			
		course_dict = zip(lecture_index,lecture_title,lecture_link)
		#print('cd1',course_dict)
		course_dict = list(course_dict)
		#print('cd2',course_dict)
		#Youtube_course = {}
		Yale_lecture_list = []

		for course_data in course_dict:
			i = list(course_data)
			#print('iii',i)
			mix_list = list(zip(keys,i))
			#print('mix_list',mix_list)
			Yale_lecture_list.append(dict(mix_list))
			youtube_course["youtube_content"] = Yale_lecture_list

		print('youtube_course',youtube_course)
		with open('yale_course_videos.json', 'w+') as wr: 
		 	wr.write(json.dumps(youtube_course, indent=4))

		return video_url	

	def run_all(self):
		r = requests.get('https://www.youtube.com/user/YaleCourses/playlists')
		page = r.text
	
		soup=BS(page,'html.parser')
		for link in soup.find_all('a'):
			str1 = link.get('href')
			if str1.find('playlist?list=') != -1:
			#	print('sting:',str1)
				self.get_course_title(str1,soup)
				

		#print(soup.prettify())
	#	with open('file.html','w+') as wr:
	#		wr.write(soup.find_all('ytd-grid-playlist-renderer'))
	#	self.get_course_title(soup)
	#	print(soup.find_all(id='items'))
if __name__ == '__main__':
	Yale_Video().run_all()
