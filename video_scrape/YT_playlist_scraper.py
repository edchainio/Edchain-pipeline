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
		url = 'http://www.youtube.com'+url1
		#print(url)
		playlist={}
		try:
			playlist =pafy.get_playlist(url)
		except:
			print("error",playlist)
		thumbnail = []
	
		count = 0
		#thumbnail = playlist.thumbnail
		listLectures = []
		
		for lectures in playlist['items']:
			# if count == 1:
			# 	break
			# count = count+1	
			listLectures.append(
				{
					"content_address":'',
					"lecture_title": lectures['playlist_meta']['title'],
					"english_transcript":'',
					"lecture_description":lectures['pafy'].description,
					"lecture_hyperlink":'https://www.youtube.com/watch?v='+lectures['pafy'].videoid,
					"ordinal_number":'',
					"lecture_thumbnail": lectures['playlist_meta']['thumbnail'],
					
					"statistics": {

						"rating": lectures['playlist_meta']['rating'],
						"views":lectures['playlist_meta']['views'],
						"likes":lectures['playlist_meta']['likes'],
						"dislikes":lectures['playlist_meta']['dislikes'],
						"keywords":lectures['playlist_meta']['keywords'],
						"runtime":lectures['playlist_meta']['length_seconds']
					
					}
					
				}

			)
 
 


		courseDict = { 	
						"unique_identifier":'',
						"content_address":'',
						"document_root":'',
						"instructor_name":'',
						"publication_date":'',
						"subject_matter":'',					
						"course_hyperlink":url,
						"course_title":playlist['title'],
						"copyright_holder":playlist['author'],
						"course_description":playlist['items'][0]['playlist_meta']['description'],
						"course_thumbnail":playlist['items'][0]['pafy'].bigthumbhd,
						"lectures": listLectures	
					}
		

		#print("content:",courseDict['lectures'][0])
		#print(playlist['items'][0]['pafy'].bigthumbhd)
		#print("contentCourseDict:",courseDict)

		return courseDict
		

	def run_all(self):
		r = requests.get('https://www.youtube.com/user/YaleCourses/playlists')
		page = r.text
	
		soup=BS(page,'html.parser')
		coursesDict=[]
		count1=0
		for link in soup.find_all('a'):
			str1 = link.get('href')
			if str1.find('playlist?list=') != -1:
				
				coursesDict.append(self.get_course_title(str1,soup))
				# count1=count1+1
				# if count1 == 10:
				# 	break

		
		with open('yale_course_videos.json', 'w+') as wr:
		 	wr.write(json.dumps(coursesDict, indent=4))		
		

		#print(soup.prettify())
	#	with open('file.html','w+') as wr:
	#		wr.write(soup.find_all('ytd-grid-playlist-renderer'))
	#	self.get_course_title(soup)
	#	print(soup.find_all(id='items'))
if __name__ == '__main__':
	Yale_Video().run_all()
