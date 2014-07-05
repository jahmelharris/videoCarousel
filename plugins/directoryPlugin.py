import os
import videoCarousel2
import threading
import pluginBase

#paths= []#['/home/rookie/Videos'] # This should come from options

class directoryPlugin(pluginBase.Plugin):
	def __init__(self, carousel):
		self.carousel = carousel
		self.files = []
		self.filterList = []
		self.paths = []
		self.stopTimer = False
		self.checkForFiles()
		self.timer = threading.Timer(2.0, self.checkForFiles)
		self.timer.start()
	def addSearch(self, path):
		self.paths.append(path)
		print("adding path "+path)

	def addFilter(self, filterVal):
		self.filterList.append(filterVal)
		print("removing "+filterVal)

	def checkForFiles(self):
		print("checking")
		print(self.paths)
		for path in self.paths:
			if(os.path.isdir(path)):
				rootdir = path
				for root, subFolders, files in os.walk(rootdir):
					if root.find("STRINGTOSEARCH") == -1: #will ignore all files containing "STRINGTOSEARCH"
						for f in files:
								#print("skipping file")
								if(self.files.count(f) == 0):
									print("adding file:")
									print(f)
									self.carousel.addFile("file://"+os.path.join(root,f))
									self.files.append(f)
					else:
						print("skipping "+ root)
		if(not self.stopTimer):
			threading.Timer(2.0, self.checkForFiles).start()

	def cleanup(self):
		self.stopTimer=True
