#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import run, PIPE
import gi, time, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Remove previous notification
run(['pkill', "notify-osd"])

cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
hasTargets, targets = cb.wait_for_targets()

# Display first 300 characters only
def shortText(text):
	if len(text) > 300: 
		text = text[:300-len(text)]
		text = text + "..."
	return text

if not hasTargets: 
	run(['notify-send', '-u', 'critical',"Clipboard is empty"])
	sys.exit()
else:
	for target in targets:
		'''
		# Uncomment below to check different gtk target types
		print(target)
		'''
		# Clipboard contains Rich Text
		if str(target) == "text/rtf":
			cbText = cb.wait_for_text()
			cbText = shortText(cbText) 
			run(['notify-send', '-u', 'critical',"Clipboard [Rich Text]", cbText])
			break
		# Clipboard contains Plain Text
		elif str(target) == "text/plain" or str(target) == "TEXT" or str(target) == "STRING" :
			cbText = cb.wait_for_text()
			cbText = shortText(cbText)
			
			# Display newline and tabs correctly in notify-send
			cbText.replace("\n", "\\n")
			cbText.replace("\t", "\\t")
			
			run(['notify-send', '-u', 'critical',"Clipboard [Plain Text]", cbText])
			break

		# Clipboard contains an Image
		elif "image/" in str(target):
			#jpegs files are generally smaller than png = faster exec
			imgType = "jpeg"
			imgPath = "/tmp/img."+imgType #Save the image in tmp folder
			cbImage = cb.wait_for_image()
			cbImage.savev(imgPath, imgType,[],[])

			run(['notify-send', '-u', 'critical' ,'-i', imgPath, "Clipboard [Image]"])
			break
