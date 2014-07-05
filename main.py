import videoCarousel2
import plugins.directoryPlugin 
import sys
import gtk
import pluginBase
def all_plugins():
	return pluginBase.Plugin.__subclasses__()

def load_plugins():
	for plugin in all_plugins():
		p = plugin(control.vidBox)
		pluginList.append(p)

def main_quit(widget):
	for plugin in pluginList:
		plugin.cleanup()
	gtk.main_quit()

def onAddFilter(widget):
	if searchBox.get_text_length() != 0:
		text = searchBox.get_text()
		if(not filterList.count(text)):
			filterList.append(text)
			for plugin in pluginList:
				plugin.addFilter(text)

def onAddSearch(widget):
	if searchBox.get_text_length() != 0:
		text = searchBox.get_text()
		if(not searchList.count(text)):
			searchList.append(text)
			for plugin in pluginList:
				plugin.addSearch(text)

if __name__=='__main__':
	searchButton = gtk.Button("+")
	filterButton = gtk.Button("-")
	filterButton.connect("clicked",onAddFilter)
	searchButton.connect("clicked",onAddSearch)
	searchBox = gtk.Entry()
	searchList = []
	filterList = []
	pluginList = []
	control = videoCarousel2.PlayerControl(int(sys.argv[1]),int(sys.argv[2]))    
	load_plugins()
	control.startVideos()	
	window = gtk.Window()                
	vbox = gtk.VBox(False,0)
	filterBox = gtk.HBox()
	
	filterBox.pack_start(searchButton, False, False)
	filterBox.pack_start(searchBox, False)
	filterBox.pack_start(filterButton,False)
	
	
	vbox.pack_start(filterBox,True,False)
	vbox.pack_start(control)
	window.add(vbox)                                           
	window.connect("destroy",main_quit)                       
	window.show_all()                                             
	gtk.main()                                                    

