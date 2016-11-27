#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import gi, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Remove previous notification
Popen(['pkill', "notify-osd"])

cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

try: # Clipboard is a string 
	cbText = cb.wait_for_text()
	# Display newline and tabs correctly in notify-send
	cbText.replace("\n", "\\n")
	cbText.replace("\t", "\\t")
	
	# Display first 300 characters only
	if len(cbText) > 300: 
		cbText = cbText[:300-len(cbText)]
		cbText = cbText + "..."
	
	Popen(['notify-send', "Clipboard Content", cbText])

except: # Clipboard is an image
	imgPath = "/tmp/img.png"
	cbImage = cb.wait_for_image()
	cbImage.savev(imgPath, "png",[],[])
	
	Popen(['notify-send', '-i', imgPath, "Clipboard Content", "[Image]"])

	#TODO: Remove tmp image after showing it

#time.sleep(5)
#Popen(['pkill', "notify-osd"])
