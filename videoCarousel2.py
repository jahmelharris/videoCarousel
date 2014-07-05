import gobject 
import gtk
import vlc
import random
import sys
import time
import os
vidWidth = 300
vidHeight = 200
instance = vlc.Instance("--aout=dummy")
class VLCWidget(gtk.DrawingArea):
    """Simple VLC widget.

    Its player can be controlled through the 'player' attribute, which
    is a vlc.MediaPlayer() instance.
    """
    def __init__(self):
        gtk.DrawingArea.__init__(self)
	self.set_can_focus(True)
	self.add_events(gtk.gdk.KEY_PRESS_MASK|gtk.gdk.BUTTON_PRESS_MASK)
        self.player = instance.media_player_new()
        def handle_embed(*args):
            if sys.platform == 'win32':
                self.player.set_hwnd(self.window.handle)
            else:
                self.player.set_xwindow(self.window.xid)
            return True
        self.connect("map", handle_embed)
	self.connect("button-press-event",self.videoClicked) #click event
        self.set_size_request(vidWidth, vidHeight)

    def videoClicked(self,widget,val): #not the best place to have this. Would prob be better creating it from the carousel
	print(self.player.get_media().get_mrl())
	self.standAlone = vlc.Instance().media_player_new(self.player.get_media().get_mrl())
	self.standAlone.play() #this plays, but will not stop on closing the window.
	return True


class multipleVideo(gtk.HBox):
	def __init__(self):
		gtk.HBox.__init__(self)
		self.playList = []
		self.players = []
	def addFile(self,filename):
		self.playList.append(filename)
	def removeFile(self,substring):
		self.tempList=  []
		for name in self.playList:
			if(name.find(substring)==-1):
				self.tempList.append(name)
		self.playList = self.tempList	
	def addPlayer(self):
		self.video = VLCWidget()
		self.players.append(self.video)
		self.add(self.video)
		self.show_all()
	#	self.pack_start(gtk.Button("button"))
		self.startPlayer(self.video.player)
	def removePlayer(self):
		self.video = self.players.pop(0)
		self.video.player.stop()
		self.remove(self.video)
	def startPlayer(self,player):
		if(len(self.playList)):
			index = len(self.playList)*random.random()
			player.set_mrl(self.playList[int(index)])
#			print("PlayList")
#			print(self.playList)
			player.play()
			player.set_position(random.random())
			

class videoCarousel(gtk.Fixed):
	def __init__(self):
		gtk.Fixed.__init__(self)
		self.row = multipleVideo()
		self.add(self.row)
		self.x = 0
		self.autoMove = False #The 2D carousel will control the movement

	def on_timer(self):
			if self.autoMove:
				self.moveRow()
				return True
			return False

	def moveRow(self,x):
		self.move(self.row,x,0)

	def addFile(self,filename):
		self.row.addFile(filename)
	def removeFile(self,substring):
		self.row.removeFile(substring)
	def addPlayer(self):
		self.row.addPlayer()

class videoCarousel2D(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		self.rows=[]
		gobject.timeout_add(10,self.on_timer)
		self.x = 0
		self.playList = []
	def addRow(self):
		self.row = videoCarousel()	
		self.rows.append(self.row)
		self.add(self.row)
		for filename in self.playList:
			self.row.addFile(filename)
	def addFile(self,filename):
		for row in self.rows:
			row.addFile(filename)
		self.playList.append(filename)
	def removeFile(self,substring):
		for row in self.rows:
			row.removeFile(substring)
	def addPlayer(self):
		for row in self.rows:
			row.addPlayer()
	def on_timer(self):
		self.x -= 1
		for row in self.rows:
			row.moveRow(self.x)
		if(self.x<0-vidWidth):
			for row in self.rows:
				row.row.removePlayer()
				row.row.addPlayer()	
			self.x = 0
	#		row.moveRow()
		return True

class PlayerControl(gtk.VBox):
	def __init__(self,x,y):
		gtk.VBox.__init__(self)
		self.vidBox = videoCarousel2D()
		self.hbox = gtk.HBox()
		self.addRowButton = gtk.Button("Add Row")
		self.addRowButton.connect("clicked",self.addRow)
		self.addColumnButton = gtk.Button("Add Column")
		self.addColumnButton.connect("clicked",self.addColumn)
		self.hbox.pack_start(self.addRowButton,False,False)
		self.hbox.pack_start(self.addColumnButton,False,False)
		self.add(self.vidBox)
		self.pack_start(self.hbox,False,False)
		self.playList = []
		self.x = x
		self.y = y
#	def addFile(self, filename):
#		self.playList.append(filename)
#	def removeFile(self,substring):
#		self.tempList = []
#		for name in self.playList:
#			if(name.find(substring)==-1):
#				self.tempList.append(name)
#		self.playList = self.tempList
#		self.vidBox.removeFile(substring)
	def startVideos(self):
		for i in range(self.y):
			self.vidBox.addRow()
#		for filename in self.playList:
#			self.vidBox.addFile(filename)
		for i in range(self.x):
			self.vidBox.addPlayer()
		self.show_all()
	def addRow(self, widget):
		self.vidBox.addRow()
	def addColumn(self, widget):
		self.vidBox.addPlayer()
def play_vid(widget):
	row.play_all()
def get_filename(path):
	print(path)
	if(os.path.isdir(path)):
		return get_filename(path+"/*")
if __name__ == '__main__':
#	window = gtk.Window()
#	row = videoCarousel2D()
#	for i in range(int(sys.argv[2])):
#		row.addRow()
#
#	for filename in sys.argv[3:]:
#		print("file is %s",filename)
#		row.addFile("file://"+filename)
#
#	for x in range(int(sys.argv[1])):
#		row.addPlayer()
#
#	#something here stops the segfaults when running multiple players :S
#	vbox = gtk.VBox()
#	b = gtk.Button("Play")
#	search = 
#	vbox.add(row)
#	vbox.add(b)	
#	window.add(vbox)
#	window.connect("destroy",gtk.main_quit)
#	window.show_all()
	control = PlayerControl(int(sys.argv[1]),int(sys.argv[2]))
#	if(os.path.isdir(sys.argv[3])):
#		rootdir = sys.argv[3]
#		for root, subFolders, files in os.walk(rootdir):
#			control.addFile("file://"+os.path.join(root,file))
#	else:
#		for filename in sys.argv[3:]:
#			control.addFile("file://"+filename)

#	control.startVideos()
#	window = gtk.Window()
#	window.add(control)
#	window.connect("destroy",gtk.main_quit)
#	window.show_all()
	#fileList.append(os.path.join(root,file))
#	if(file.endswith(".jpg")):
#		break
#	if(file.endswith(".png")):
#		break
#	control.removeFile("random") 
#	gtk.main()
