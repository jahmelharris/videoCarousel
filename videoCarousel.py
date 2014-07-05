import random
import gtk
import vlc
import sys
instance = vlc.Instance("--aout=dummy")
vidWidth = 320
vidHeight = 200
startPlay = 2
class VLCWidget(gtk.DrawingArea):
    """Simple VLC widget.

    Its player can be controlled through the 'player' attribute, which
    is a vlc.MediaPlayer() instance.
    """
    def __init__(self, *p):
        gtk.DrawingArea.__init__(self)
	self.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color(int(random.random()*255),int(random.random()*255),int(random.random()*255)))
        self.player = instance.media_player_new()
        def handle_embed(*args):
            if sys.platform == 'win32':
                self.player.set_hwnd(self.window.handle)
            else:
                self.player.set_xwindow(self.window.xid)
            return True
        self.connect("map", handle_embed)
        self.set_size_request(vidWidth, vidHeight)

class videoCarouselRow(gtk.Fixed):
	def __init__(self):
		gtk.Fixed.__init__(self)
		self.numberOfPlayers = 0
		self.videoPlayers = []
		self.playList = []
		self.x = 0
		gtk.timeout_add(20,self.on_timer)
		#self.sizeOfControl = gtk.Button("button").size_request()[0]	
		self.sizeOfControl = vidWidth
	
	def resize(self,xSize):
		if(xSize > self.numberOfPlayers):
			for i in range(xSize-self.numberOfPlayers-1):		
				self.__pushPlayer()
			self.size = self.size_request()
			self.__pushPlayer()
			print("setting size")
			print(self.size)
			self.set_size_request(vidWidth*(xSize-1),vidHeight)
			
		else:
			for i in range(xSize-self.numberOfPlayers,0):
				self.__removePlayer()
		self.numberOfPlayers = xSize
	def addPlayer(self):
		self.resize(self.numberOfPlayers+2)	
	def __removePlayer(self,player=0):
		self.remove(self.videoPlayers.pop(player))
		self.x -= self.sizeOfControl
	def __pushPlayer(self):
		print("adding player x=",self.x)
		player = VLCWidget()
		self.videoPlayers.append(player)
		if(len(self.get_children())):
			self.position = self.child_get_property(self.get_children()[-1],"x")+self.sizeOfControl-1
		else:
			self.position = 0
		self.add_with_properties(player,"x",self.position,"y",0)
		self.x += self.sizeOfControl;
		self.play(player)
	
	def on_timer(self, *args):
		for player in self.get_children():
			x = self.child_get_property(player,"x")
			self.move_player(player,x-1)
	#		if(self.child_get_property(self.videoPlayers[-1],"x")+self.sizeOfControl < self.size_request()[0]):
	#			self.__pushPlayer()
#			player.show_all()
	#	window.show_all()
		self.show_all()
		return True

	def play(self,vlcInstance):
		if(len(self.playList)):
			self.item = int(random.random()*len(self.playList))
			vlcInstance.player.set_mrl(self.playList[self.item])
			vlcInstance.player.audio_set_volume(0)
			vlcInstance.player.play()

	def move_player(self,widget,x):
		self.move(widget,x,0)
		self.child_set_property(widget,"x",x)
		if(x<0-self.sizeOfControl):
			print("removing player")
			self.__removePlayer(0)
			widget.player.stop()
			self.__pushPlayer()	
	def addFile(self,filename):
		self.playList.append(filename)

class videoCarouselMultiRow(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		self.playList = []
		self.rows = []
		self.sizeOfControl = vidWidth
	def addRow(self,numberOfRows=1,numberOfVideos=2):
		for i in range(numberOfRows):
			row = videoCarouselRow()
			for filename in self.playList:
				row.addFile(filename)
			row.resize(numberOfVideos)
			self.rows.append(row)
			self.add(row)

	def addFile(self,filename):
		self.playList.append(filename)
	
	def setSize(self,size):
		self.set_size_request(size[0],size[1])
		for row in self.rows:
			row.set_size_request(size[0],vidHeight)
def addRow(wid):
	v.addRow()

def addColumn(wid):
	for player in v.rows:
		player.addPlayer()
if __name__=='__main__':
	
	vbox = gtk.VBox()
	v = videoCarouselMultiRow()
	v.addFile("file:///home/rookie/blink.flv")
	v.addFile("file:///home/rookie/smandowhatiwant.flv")
	v.addFile("file:///home/rookie/sweetieBot.flv")
	v.addFile("file:///home/rookie/videoSample.flv")
	v.addFile("file:///home/rookie/whenimmagic.flv")
	v.addFile("file:///home/rookie/whenimrandom.flv")
	v.addRow(1,5)
	vbox.pack_start(v)
	button = gtk.Button("addRow")
	button2 = gtk.Button("addColumn")
	vbox.pack_start(button,False)
	vbox.pack_start(button2,False)
	window = gtk.Window()
	window.connect("destroy",gtk.main_quit)
	button.connect("clicked",addRow)
	button.connect("clicked",addColumn)
	window.add(vbox)
#	window.connect("check-resize",resize_image)
	window.show_all()
	gtk.main()
#	v.cleanup()

