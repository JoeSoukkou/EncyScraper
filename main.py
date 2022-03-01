from __future__ import ( division, absolute_import, print_function, unicode_literals )
import sys
import os 
from PySide2 import *
from bs4 import BeautifulSoup 
import requests
from ui_Ency_Web_Scraper_Interface import * 
import tempfile, logging
import urllib.request as urllib2
import urllib.parse as urlparse

rootUrl = "http://univ.ency-education.com"
moduleYearDict = {4 : ["Cardiologie","Gastro-entérologie","Mal﻿adies infectieuses","Neurologie","Onco-Hématologie","Pneumologie-Phtisiologie"], 5 : ["Endocrinologie","Gynécologie","Orthopédie","Pédiatrie","Psychiatrie","Rhumatologie","Urologie-Nephrologie"], 6 : ["Urgences médico-chirurgicales","Thérapeutique","Psychologie médicale","ORL","Ophtalmologie","Médecine de travail","Médecine légale","Épidémiologie","Économie","Droit et déontologie médicale ","Dermatologie"]}
downloadingStatus = False

def DownloadClicked():
	# Check if a subject has been selected from the dropdown menu +++
	# Use subject to lookup which year it is from +++
	# Construct target URL +++
	# If successful, start scraping that URL for the proper links by calling another function +++ 
    
	subject = getSelectedSubject()
		
	year = subjectYearLookup(subject)
	if year : 
		URL = "{rooturl}/medecine_{theyear}an-exams.html".format(rooturl = rootUrl,theyear = year)
		Scraper(URL, subject)
			

def subjectYearLookup(subject):
	for year in moduleYearDict :
		for Subject in moduleYearDict[year]:
			if subject == Subject : 
				return year		

def Scraper(URL, subject): 
	global downloadingStatus
	try:
		#Disable the download button
		download_button.setEnabled(False)
		cancel_button.setEnabled(True)
		
		page = requests.get(URL)
	
		# CORE SHIT STARTS HERE
		soup = BeautifulSoup(page.content, 'html.parser')
		linkList = []
		
		
		downloadingStatus = True

		for u in soup.find_all('u'):
			if(u.get_text() == subject):
				div = u.find_next("div")
				for link in div.find_all('a'):
					scrapedUrl = link.get('href')
					fullUrl = "{root}{url}".format(root= rootUrl, url=scrapedUrl)
					linkList.append(fullUrl)
				break			
		for i in linkList :	
			QtCore.QCoreApplication.processEvents()
			fileBeingDownloaded = i.split("/")[-1]
			updateTelemetry(fileBeingDownloaded)
			feedback = "Downloading [{0}/{1}] Files".format(linkList.index(i)+1,len(linkList))
			#Download file function call
			if (downloadingStatus == True) :
				updateFeedback(feedback) 
				downloadFile(i, fileBeingDownloaded)
			else : 
				break	
			
		# CORE SHIT ENDS HERE
		
	except : 
		updateFeedback("Check your internet !")

def downloadFile(url, filename):
	global downloadingStatus
	""" 
    Download and save a file specified by url to dest directory,
    """
	u = urllib2.urlopen(url)

	scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
	
	
	dest = os.getcwd()

	with open(filename, 'wb') as f:
		QtCore.QCoreApplication.processEvents()
		meta = u.info()
		meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
		meta_length = meta_func("Content-Length")
		file_size = None
		if meta_length:
			file_size = int(meta_length[0])
		

		file_size_dl = 0
		block_sz = 8192
		while True: 
			QtCore.QCoreApplication.processEvents()
			buffer = u.read(block_sz)
			if not buffer:
				break
			if not downloadingStatus : 
				break 

			file_size_dl += len(buffer)
			f.write(buffer)

			percentage = int(file_size_dl * 100 / file_size)
			updateProgressBar(percentage)
        

def abort():
	global downloadingStatus
	#Abort logic in here
	downloadingStatus = False
	updateProgressBar(0)
	updateFeedback("Download aborted !")
	cancel_button.setEnabled(False)
	download_button.setEnabled(True)
	 

class MainWindow(QMainWindow):
 	def __init__(self):
 		QMainWindow.__init__(self)
 		self.ui = Ui_MainWindow()
 		self.ui.setupUi(self)
 		self.show()
 		
if __name__ == '__main__':

	app = QApplication(sys.argv)
	window = MainWindow()
	
	def updateFeedback(feedback):
		window.ui.Feedback_Text.setText(feedback)

	def updateTelemetry(fileBeingDownloaded): 
		window.ui.File_Being_Downloaded.setText(fileBeingDownloaded)

	def updateProgressBar(progress):
		window.ui.Progress_Bar.setValue(progress)

	def getSelectedSubject():
		#Dropdown menu wiring
		dropdown_menu = window.ui.Select_Modules_Dropdown
		selected_subject = dropdown_menu.currentText() 
		return selected_subject
	
    #Download button wiring
	download_button = window.ui.Download_Button
	download_button.clicked.connect(DownloadClicked)
 		 	
	#Abort Button wiring 
	cancel_button = window.ui.abortButton
	cancel_button.clicked.connect(abort)
	cancel_button.setEnabled(False)

	sys.exit(app.exec_())



