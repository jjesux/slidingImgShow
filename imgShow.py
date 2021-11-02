

"""
 This python application is used to display amd swap images. It can also delete
 images. It can also rename images one by one or o many of them like only one 
 operation.
 These images may be on  a directory, and their paths are copied into a list of
 strings. After this the images are displayed on the window application GUI 
 interface, looping through the whole list of image files. The looping can be 
 set to move forward or backward on list.
 Image files can be deleted one by one. This action cannot be undone.
 Image file names can be change. This action cannot be undone. In order to 
 undone this action the file name has to be renamed with the old file name.
 The delay time can also be changed, increased or decreased. This delay time 
 sets the time that an image is displayed before been swapped.
 The directory where the images are can be changed or selected a different one 
 at any time. 
 The application can be paused. The images will not be swapped. The images swap 
 movement can be forward or backward, manually, one by one.

 10/23/2021 10:00 am.
"""



# Importing libraries to complete this image show project.
import glob
import os
import time
from tkinter import font
# Libs to manage images and switch images
from PIL import Image, ImageTk, ImageDraw, ImageFont
# Libs to manages GUI widges
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk, Toplevel
from tkinter.ttk import Frame, Label, Button, Spinbox
# Class is used to manage direectory and file access. 
from imgShowCntrl import imgShowCtrlClass




"""
Class Window is used to drive the whole process that this app performs.
This class sets all the widgets that are used in this app.
This class sets all the local variables used to manage the diferent states that
this app can be in. These states are playing or paused.
Other local variables are also used to managed and set the different text and 
button colors. Other local variables are used to set the path of the image files
that are swapped.
"""
class Window(Frame):


	"""
	This function is used to initialize all the variables that are used  in this 
	class. It also call another function that create the whole GUI and their 
	componentes.
	"""
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		# Creating the class that will access directory to get the image files.
		self.cntrlClass = imgShowCtrlClass()
		self.cntrlClass.setRef(self)


		# Set of widget style configurations to customize buttons
		self.myStyle = ttk.Style()
		self.myStyle.configure('blue.TButton', background='#0000FF', foreground='#0000FF')
		self.myStyle.configure('red.TButton', background='#FF0000', foreground='#FF0000')
		self.myStyle.configure('green.TButton', background='#20F2B8', foreground='#20F2B8')
		# boolean to set the play button to red when the playing show is paused
		self.greenBlue = False


		# Setting the call back function when the key 'q' is clicked.
		# This function is defined as a class method.
		self.bind_all('q', self.do_exit)


		# This variable holds the file name of the file that is used to resize the 
		# images before being swapped. Doing so the original image is not altered.
		self.tmpFileName = 'resizedPic.png'
		# This variable holds the directory path where all the image files are.
		self.strPath = ''

		# Setting the path list of image files to be displayed, but this list is 
		# only used to manage the first image and the image that it is show when 
		# the directory is empty.  It will hold only one file at any time.
		self.imgNames = []
		# This variable contains the size of the real list of files that exist 
		# in the directory selected. This list is manage by the controling class.
		self.imgNamesSize = 0
		
		# List of image files index is set to -1, so when this app starts it 
		# is increment by one.
		self.index = -1
		# Boolean to set the direction of the picture movement; forward is True  
		# and backward is False.
		self.nextBackMode = True
		# This variable holds the image file beeing displayed.
		self.photo = None
		# Setting the status of the playing action; playing is True and paused
		# is False.
		self.playingStatus = False
		# Setting the time to display the next picture. 1000 == 1 sec.
		self.delay = 1000
		# Setting the image height, and from this value the image width.
		self.baseHeight = 650
		# This variable holds the Label widget where the image will be displayed.
		self.labelPicture = None
		# A temporary image file to swap the images that are displayed. 
		# The present and the next or back image.
		self.labelPicture_old = None
		# Variable to hold the path image and file name. This is mainly for 
		# debugging.
		self.txtFileInfo = tk.StringVar()
		# Variable to hold the number-index of the image been shown.
		self.txtFileIndx = tk.StringVar()
		# Variable used in the Spinbox to hold a value to increase or decrease 
		# the delay time.
		self.delayChangeBy = tk.IntVar()
		# Variable to hold the new file name when a file is renamed.
		self.picName = tk.StringVar()
		###########Como que esta variable no se usa. Solo checarla bien
		# Creo que se usan para el multirenaming process
		self.XXXXXXXXXnumberIncrease = tk.IntVar()
		###########Como que esta variable no se usa. Solo checarla bien
		# Creo que se usan para el multirenaming process
		self.charsToAdFName = tk.StringVar()
		# Variable used to change the app state from playing to pause and vice 
		# versa. Its values are 'p' == playing and 's' == paused
		self.mStrCmd = ''
		# Variable used to know in which state the app is at any moment.
		self.edoPlaying = False

		# if statement to set how the app starts. If there is any images in the 
		# list of images, then it starts showing those images.
		if len(self.imgNames) >= 1:
			self.createWidgets()
		# If list is empty, then this app creates an image letting user know that.
		# User has to select the directory of images to display.
		else:
			# Creating the first image to display when there is not any image.
			self.createMyInitialImage("Hello My Lord Nicky.  Please Make Your Selection")
			# Creating the main window and all the widgets that are in it.
			self.createWidgets() 


		# These variables are used to rename many file like only one operation.
		# List of image files to hold the files to be renamed.
		# NOTE: Creo que no se usa ya en esta ultima version.
		self.fileListToRename = []
		# Boolean to know in which mode the app is.
		self.appMultiRenameMode = False
		# Dictionary to hold the index and the image file path. 
		# key==index, value==file Path.
		self.pathFileDict = {}
		# Integer number to add to the file name. This number will be increased
		# by one on each different file renamed.
		self.numberIncrease = tk.IntVar()
		# NOTE: Talvez seria bueno elimiar esta variable,,,,,,,,,,,,,,,,,,,,,,
		self.similarNames = []


	# End of __init__() class constructor function.




	"""
	createWidgets(self) function class is used to set and configure all the main 
	window widgets.
	"""
	def createWidgets(self):
		# print('Function  -  createWidgets(self)')

		# Button used to set the images directory path.
		self.setDirBtn = Button(self, text="[Op]", style="blue.TButton", width=5,  command=self.setDirectorio)
		self.setDirBtn.grid(row=0, column=0, sticky=tk.NW) 

		# Spinbox used to set the delta time when the delay time needs to be 
		# changed.
		self.delayTimeSB = Spinbox(self, from_=-19, to=60, increment=1, textvariable=self.delayChangeBy, width=3, state="disable", command=self.onSetDelayTime)
		self.delayTimeSB.grid(row=1, column=0, sticky=tk.NW, padx=2)

		# Button to set the app movement direction backward. Code to configure 
		# button settings.		
		self.backBtn = Button(self)
		self.backBtn.grid(row=2, column=0, sticky=tk.NW)
		self.backBtn["text"] = "[<B]"
		self.backBtn["width"] = 5
		self.backBtn["command"] = self.backPicture
		self.backBtn["style"] = "blue.TButton"
		self.backBtn["state"] = "disable"

		# Button to set the app on playing or paused mode.
		self.playBtn = Button(self, text="[<>]", style="blue.TButton", width=5, state="disable", command=self.playShow)
		self.playBtn.grid(row=3, column=0, sticky=tk.NW)

		# Button to set the app movement direction forward.
		self.forWardBtn = Button(self, text="[N>]", style="blue.TButton", width=5, state="disable", command=self.nextPicture)
		self.forWardBtn.grid(row=4, column=0, sticky=tk.NW)

		# Button to start the file renaming process.
		self.renameBtn = Button(self, text="[Re]", style="blue.TButton", width=5, state="disable", command=self.renamePicture)
		self.renameBtn.grid(row=5, column=0, sticky=tk.NW, pady=0)

		# Button used to delete an image file from the device.
		# Note: This action cannot be undone.
		self.deleteBtn = Button(self, text="[De]", style="red.TButton", width=5, state="disable", command=self.deletePicture)
		self.deleteBtn.grid(row=6, column=0, sticky=tk.NW)

		# Button to shut off the app.
		self.quitBtn = Button(self, text="[X]", style="red.TButton", width=5, command=self.doExit)#command=self.master.destroy)
		self.quitBtn.grid(row=7, column=0, sticky=tk.NW)

		# Label widget to display a label with information about the image being
		# displayed. This shows file path data.
		self.labelInfo = Label(self, background="white", textvariable=self.txtFileInfo, font=("TkDefaultFont", 9), wraplength=600)
		self.labelInfo.grid(row=8, column=0, sticky=tk.NW, columnspan=5)

		# Label widget to display a label with the index-number of the imagen that
		# it is being displayed.
		self.labelIndxInfo = Label(self, textvariable=self.txtFileIndx, font=("TkDefaultFont", 8), wraplength=30)
		self.labelIndxInfo.grid(row=8, column=1, sticky=tk.NE, columnspan=1)

		self.resizingPicture()
		
	# End of createWidgets() class function.




	"""
	createMyInitialImage() function is used to create an image with text in it.
	This text is a greeting to the user. This image is displayed when the app 
	starts. It is also displayed when there are not more images to display.
	"""
	def createMyInitialImage(self, strMsg):
		# print('Funcion  -  createMyInitialImage()')

		# App is creating an image with some text on it.
		imgTmp = Image.new('RGB', (600, 500), color=(0, 0, 250))
		fntTmp = ImageFont.truetype('Gabriola.ttf', 35)
		picTmp = ImageDraw.Draw(imgTmp)
		# The text in the image.
		picTmp.text((15, 100), strMsg, font=fntTmp, fill=(255, 0, 0))
		imgTmp.save('tmpPic.png')
		# Setting a temporary image path.
		strPathTmp ="tmpPic.png"
		# Setting the application display movement direction.
		# Setting the real image path + name to be displayed. 
		self.imgNames = [os.path.join(os.getcwd(), strPathTmp)]
		self.imgNames = [self.imgNames[0].replace('\\', '/')]
		#print(os.getcwd())

	# End of createMyInitialImage() class function.




	"""
	resizingPicture() function is used to change the size of the image to fit 
	the main window height. Then it set the image into the Label widget to be 
	displayed.
	"""
	def resizingPicture(self):
		# print('Funcion  -  resizingPicture()')

		# If list of images is not empty, then display images on the images list.
		if len(self.imgNames) >= 1:
			try:
				# Opening the image file.
				self.img = Image.open(self.imgNames[self.index])
			except (IOError, OSError):
				# caching any error while opening the file.
				# Faltaria crear un message warning to the user.
				print("Error Open File At Index: " + str(self.index))
				print(IOError.strerror )


			# Resizing the height and width size of the image.
			hPercent = (self.baseHeight / float(self.img.size[1]))
			widthSized = int(float(self.img.size[0]) * float(hPercent))
			self.img = self.img.resize((widthSized, self.baseHeight), Image.ANTIALIAS)
			# Getting  colored image to be displayed.
			self.photo = ImageTk.PhotoImage(self.img)
			self.img.close()
			# Setting the image to be displayed on a label widget.
			self.labelPicture = Label(self, image=self.photo)
			self.labelPicture.image = self.photo
			# Setting position of the label containing the image. 
			self.labelPicture.grid(row=0, column=1, sticky=(tk.N + tk.S), rowspan=8)
			# VER QUE ES LO QUE PASA AQUI. SIN ESTO NO TRABAJA EL PROG.
			if self.labelPicture_old is not None:
				self.labelPicture_old.destroy()
			self.labelPicture_old = self.labelPicture

		else:
			# Warnig the user about the selected directory being empty.
			self.txtFileInfo.set("There is not pictures in directory")
			self.labelInfo.configure(background="red")

	# End of resizingPicture() class function.




	"""
	on_setDelayTime(self) class callback function is used to change the delay 
	time used to swap images. This callback function is called when the Spinbox 
	widget is clicked to increased or decrease the swapping time.  The lowest 
	time is 50 milliseconds. The highest is 5.5 seconds.
	"""
	def onSetDelayTime(self):
		# print('Function  -  onSetDelayTime(self)')

		# Variable to always used the default delay time, even when the delay 
		# var is changed.
		loopingTime = 1000
		# if block to prevent that delay gets a value of zero.
		if self.delay > 50:
			# Setting the delay time new value.
			self.delay = loopingTime + (self.delayChangeBy.get() * 50 )

	# End of on_setDelayTime(self) class function.
	



	"""
	setBtnsImgsDirection() function is used to synchronize the text and color 
	of the buttons that are affected wether the app is in paused mode or moving 
	and displaying images mode. Some of these buttons are also affected by the 
	direction of the app. This movement traversing the image list maybe forward 
	or backward.
	"""
	def setBtnsImgsDirection(self):	
		# print('Funcion  -  setBtnsImgDirection()')

		# Sliding movement is ON
		if self.playingStatus == True:
			# movement is forward -->
			if self.nextBackMode:
				self.playBtn["text"] = ">>>>"
				self.forWardBtn["style"] = "green.TButton"
				self.backBtn["style"] = "blue.TButton"
			# Movement is backward <--
			else:
				self.playBtn["text"] = "<<<<"
				self.backBtn["style"] = "green.TButton"
				self.forWardBtn["style"] = "blue.TButton"

			self.playBtn["style"] = "blue.TButton"
			# Button to delete files is disabled while the app is in playing mode.
			self.deleteBtn["state"] = "disable"
			# Button to rename files is disabled while the app is in playing mode.
			self.renameBtn["state"] = "disable"
		# Slidinig movement is paused
		else:
			print('PAUSANDO LA SWAPPING SHOW.........')
			#pausar el movimiento de las fotos.
			self.playBtn["text"] = "[<>]"
			self.playBtn["style"] = "red.TButton"
			# Button to delete files is enabled while the app is in playing mode.
			self.deleteBtn["state"] = "normal"
			# Button to rename files is enabled while the app is in playing mode.
			self.renameBtn["state"] = "normal"

			#print('del next::: ' + str(self.nextBackMode))
			#if self.nextBackMode:
			#	self.forWardBtn["style"] = "green.TButton"
			#	self.backBtn["style"] = "blue.TButton"
			## Movement is backward <--
			#else:
			#	self.backBtn["style"] = "green.TButton"
			#	self.forWardBtn["style"] = "blue.TButton"



	# End of setBtnsImgsDirection(self) class function.




	"""
	pausePlayShow() function is used to set the app in paused mode. Images are 
	not swapped.
	"""
	def pausePlayShow(self):
		# print(Function  -  pausePlayShow(self)')

		# variable playingStatus in paused mode is == False.
		if self.playingStatus:
			self.mStrCmd = 's'
			self.playingStatus = False
			# Setting widgets to let user the app is paused.
			self.setBtnsImgsDirection()

	# End of pausePlayShow(self) class function.




	"""
	setDirectorio() function is used to let user to select a directory with 
	image files to display. It shows user a window with which the user can 
	navigate to the directory where images are saved. It set the app in paused 
	mode before showing the select directory window.
	"""
	def setDirectorio(self):
		# print('Function  -  setDirectorio()')

		# Setting the app in paused mode.
		self.pausePlayShow()
		# Getting the directory path.
		self.strPath = dirName = tk.filedialog.askdirectory()
		# if block to handle the cancelation of directory selection.
		if dirName == '':
			if self.playingStatus and self.imgNamesSize > 0:
				self.mStrCmd = 'p'
				# Starting, again, the images swapping process.
				self.playShowDriver()
			else:
				# NOTE: TO DO:	Talvez seria bueno mostrar un warning on ERROR.
				print('DIRECTORY NAME is null. Cancel btn was clicked.  ---> imgShow.py')
		# else block to handle the directory selection.
		else:
			# Passing the directory path to the controling class.
			self.imgNamesSize = self.cntrlClass.setDirectoryPath(dirName)
			self.index = 0
			self.mStrCmd = 's'		#stop or paused the image sliding 
			# Setting the default swap direction forward.
			self.nextBackMode = True
			# Swapping the next image.
			self.playShowHelper()
			# There are some widgets that are enable when app is in paused mode.
			#self.setBtnsImgsDirection()
			self.disableEnableWidgetBtns()

			if self.nextBackMode:
				self.forWardBtn["style"] = "green.TButton"
				self.backBtn["style"] = "blue.TButton"
			## Movement is backward <--
			else:
				self.backBtn["style"] = "green.TButton"
				self.forWardBtn["style"] = "blue.TButton"


			self.labelInfo.configure(background="white")

	# End of setDirectorio(self) class function.




	"""
	playShow() callback function is called when the play button is clicked.
	This function move the app from the paused state to the playing state. Then 
	it sets the button text that are affected by the change of app state. Then 
	it calls another that actually start the looping process to swap images.
	"""
	def playShow(self):
		# print('Function  -  playShow()')

		# if block to move the app from the paused state to the playing state.
		if self.edoPlaying == False:
			self.edoPlaying = True
			self.mStrCmd = 'p'
			self.playingStatus = True
		# else block to move the app from the playing state to the paused state.
		elif self.edoPlaying:
			self.edoPlaying = False
			self.mStrCmd = 's'
			self.playingStatus = False
		# NOTE: TO-DO Creo que aqui se debe de poner algun tipo de warnig to the 
		# user.
		else:
			self.mStrCmd = ''
		# Changing the widget text from paused to playing and vice versa.
		self.setBtnsImgsDirection()

		self.playShowDriver()

	# End of playShow(self) class function.




	"""
	playShowDriver(self) function is called to actually start and traverse the 
	list of image files calling itself until the play button is clicked setting 
	the app in paused mode.
	"""
	def playShowDriver(self):
		# print('Function  -  playShowDriver()')

		# if block to set the app in paused mode.
		if self.mStrCmd == 's':
			self.edoPlaying = False
			self.playingStatus = False
		# elif block to set the app in playing mode.
		elif self.mStrCmd == 'p':
			self.edoPlaying = True
			self.playingStatus = True
			# Setting the widgets that are affected by the app state change.
			self.setBtnsImgsDirection()
			# Increasing-decreasing the index to show the next image.
			self.setIndex()
			# Calling the function that actually swap and show the next image.
			self.playShowHelper()
			# Calling itself to show the next image.
			self.after(self.delay, self.playShowDriver)
		# NOTE: TO-DO: Maybe poner un warning para los users.
		else:
			print('Something went wrong with in funcion playShowDriver()')
		
	# End of playShowDriver(self) class function.
		



	"""
	playShowHelper(self) function is used to actually display the image on the 
	app main window using a label widget. It also catch error relating to open 
	files, index out of range or directories being empty. This function does 
	not retrieve files from the selected directory.
	"""
	def playShowHelper(self):
		# print('Function  -  playShowHelper()')
		
		# Invoking a function that is member of another class to access the 
		# selected directory to retrieve the image file. It returns a list 
		# containing info about the image file to be displayed.
		indexPhotoLst = self.cntrlClass.showImagenCntrl(self.index)

		# if block to actually set the file image on a label widget to be 
		# displayed.
		if indexPhotoLst[0] >= 0 and len(indexPhotoLst[1]) > 0: 
			# WARNING...No se debe de alterar self.strPath ya que su valor no 
			# debe de cambiar once a directory is selected.
			#self.strPath = indexPhotoLst[1]
			# Getting the photo file from the returned list into a local var.
			self.photo = indexPhotoLst[2]

			# destroyig the label that hold the previous image, and it will 
			# hold the new image.
			if self.labelPicture is not None:
				self.labelPicture.destroy()

			# Setting the image to be displayed on a label widget.
			self.labelPicture = Label(self, image=self.photo)
			self.labelPicture.image = self.photo
			# Setting position of the label containing the image. 
			self.labelPicture.grid(row=0, column=1, sticky=(tk.N + tk.S), rowspan=8)
			# Setting the displayed imagen file path information label.
			self.txtFileInfo.set("FN: " + indexPhotoLst[1])	#self.strPath)
			# Setting the displayed image index-number information label.
			self.txtFileIndx.set(self.index)
			# VER QUE PASA AQUI.
			if self.labelPicture_old is not None:
				self.labelPicture_old.destroy()
			self.labelPicture_old = self.labelPicture
		# else block to catch errors.
		else:
			# if block related to directories being empty.
			if indexPhotoLst[0] == -2:
				# Creating an image to let user know that the selected directory 
				# is empty, or the index is out of range.
				self.createMyInitialImage("My Lord Nicky. \nThere are not more images to show or to delete. \nPlease select another directory.")
				# Changing the image size to fit the app main window.
				self.resizingPicture()
			# elif block to catch errors relating to file opening.
			elif indexPhotoLst[0] == -1:
				# Creating a warning dialog to warn user about OS errors.
				self.createWarningDialog(indexPhotoLst[1], 1)
				# Setting the app in paused mode
				if self.playingStatus:
					self.mStrCmd = 's'
					self.playingStatus = False
					# Setting widget text for the app change to paused mode.
					self.setBtnsImgsDirection()

	# End of playShowDriver(self) class function.

			


	"""
	disableEnableWidgetBtns(self) function is used to enable or disable some of 
    the button widgets when the app change the state from paused to playing .
	"""
	def disableEnableWidgetBtns(self):
		# print('Function  -  disableEnableWidgetBtns(self)')

		self.delayTimeSB["state"] = "normal"
		self.backBtn["state"] = "normal"
		self.playBtn["state"] = "normal"
		self.forWardBtn["state"] = "normal"
		# these buttons are disable when the app is playing.
		if self.playingStatus is False:
			self.renameBtn["state"] = "normal"
			self.deleteBtn["state"] = "normal"

	# End of disableEnableWidgetBtns(self) class function.




	"""
	backPicture(self) class callback function is used to set the application
	movement backward.
	"""
	def backPicture(self):
		# print('Function  -  backPicture(self)')

		# if statement to set the application movement backward.
		if self.imgNamesSize >= 1:
			# Setting sliding direction to backward movement
			if self.nextBackMode == True:
				self.nextBackMode = False
				# Changing the play text only if app mode is not in pause mode.
				self.forWardBtn["style"] =  "blue.TButton"
				self.backBtn["style"] = "green.TButton"
				if self.playingStatus:
					self.playBtn["text"] = "<<<<"
				else:
					self.playBtn["text"] = "<<<>"
			# if app is in pause mode, then show previous image. 
			# App is starting the sliding image show, 
			if self.playingStatus == False:
				self.setIndex()
				self.playShowHelper()

		#  else statement to show debugging info.
		else:
			# Show user that an error has appear on the scren.`
			print("imgNames size esta mas bajo que zero")

	# End of backPicture(self) function.




	"""
	nextPicture(self) class callback function is used to set the application 
	movement forward.
	"""
	def nextPicture(self):
		# print('Function  -  nextPicture(self)')

		# if statement to set the application movement forward.
		if self.imgNamesSize >= 1:
			# Changing the play text only if app mode is not in pause mode.
			if self.nextBackMode == False:
				self.nextBackMode = True
				self.forWardBtn["style"] = "green.TButton"
				self.backBtn["style"] = "blue.TButton"
				# Playing mode.
				if self.playingStatus:
					self.playBtn["text"] = ">>>>"
				# Paused mode.
				else:
					self.playBtn["text"] = "<>>>"
			# if app is in pause mode, then show the next image. 
			# App is starting the sliding image show, 
			if self.playingStatus == False:
				self.setIndex()
				self.playShowHelper()
		#  else statement to show debugging info.
		else:
			# Show user that an error has appear on the scren.`
			print("imgNames size esta mas bajo que zero")

	# End of nextPicture(self) function.




	### Start of the renaming files code.




	"""
	createRenameDialog(self) callback function is invoked when the rename button
	on the main window is clicked by the user. This function creates a dialog 
	to give user some options about renaming files. These options are rename one
	file, or rename multiple files or cancel the whole process.
	"""
	def createRenameDialog(self):
		# print('Function  -  createRenameDialog(self)')

		# Global variables to get the new file name and to handle the dialog 
		# window.
		# Creating the dialog main window.
		self.miniWindow = Toplevel(master=imgShowApp)
		self.miniWindow.title(' - miniWindow - Rename Image File')
		self.miniWindow.attributes("-topmost", True)

		# Two label to instruct users what to do on the dialog interface.
		labelMultiInfoTmp1 = tk.Label(master=self.miniWindow, text='To rename multi images, click multImg button.')
		labelMultiInfoTmp1.grid(row=0, column=0, sticky=tk.W, columnspan=3)
		# More information to the user about what to do.
		labelInfoTmp1 = tk.Label(master=self.miniWindow, text='Enter New Picture Name:')
		labelInfoTmp1.grid(row=1, column=0, sticky=tk.W, columnspan=3)
		labelInfoTmp2 = tk.Label(master=self.miniWindow, text='Don\'t type file extension. It\'ll be added.')
		labelInfoTmp2.grid(row=2, column=0, sticky=tk.W, columnspan=3)

		# Entry widget to get the new file name entered by users.
		self.entry = ttk.Entry(master=self.miniWindow, textvariable=self.picName)
		self.entry.grid(row=3, column=0, sticky=tk.W, columnspan=2)

		# Button to start the file renaming process.
		btnChangeName = ttk.Button(master=self.miniWindow, text='Cambiar', command=self.cambiarNombre)#, state=tk.DISABLED)
		btnChangeName.grid(row=4, column=0, sticky=tk.W)

		# Button to select the option to rename multiple files.
		btnMultiChangeName = ttk.Button(master=self.miniWindow, text='MultImg', command=self.cambiarMultiNombres)
		btnMultiChangeName.grid(row=4, column=1, sticky=tk.W)

		#Button to cancel the file renaming process.
		btnCancel = ttk.Button(master=self.miniWindow, text='Cancel', command=self.cancelarCambiarNombre)
		btnCancel.grid(row=4, column=2, sticky=tk.W)

	# End of createRenameDialog(self) function.	




	"""
	renamePicture(self) callback function is invoked when the rename button on 
	the main window app is clicked. This function checks that the directory is 
	not empty and that the file exit. If so, then it calls another function to
	create a dialog to get the new file name and start or cancel the renaming 
	process.
	"""
	def renamePicture(self):
		# print('Function  -  renamePicture()')

		# Warning user that renaming a picture can be done only when the app is 
		# on paused mode. 
		# I think the program never enter this part of the if-else block
		if self.playingStatus == True:
			print("To rename a picture set the app on Paused Mode.")
		else:
			# Starting renaming process.
			# Checking that path name list is not empty.
			if self.imgNamesSize > 0:	 
				# Making sure that the picture file exist.
				if self.cntrlClass.doesImageExist(self.index): 
					# Call function to create dialog to get new file name.
					self.createRenameDialog()

				#Trying to catch the file does not exist error with if-else.
				else:
					# # I think the program never enter this part of the if-else block
					print("The file that is been renamed does not exist on this folder.")
					print("Exiting the renamePicture function.")
					#self.createWarningDialog('The file that is been renamed does not exist on this folder.')
					return

	# End of renamePicture(self):function.




	"""
	createWarningDialog(self, strWarning, mMaster) function is used to build a 
	dialog to let user about errors that happend during the renaming process, and 
	to let user know that new file name cannot be empty, and errors about the 
	directory being empty.
	"""
	def createWarningDialog(self, strWarning, mMaster):
		# print('Function  -  createWarningDialog(self, strWarning, mMaster)')

		# if block about OS Errors.
		if mMaster == 1:
			self.miniWindow2 = Toplevel(master=imgShowApp)
			btnOKTmp = tk.Button(master=self.miniWindow2, text='OK', command=self.noNameRenameWarningX)
			btnOKTmp.grid(row=2, column=0, sticky=tk.W, columnspan=1)
		# else block about empty directory of empty string.
		elif mMaster == 2:
			self.miniWindow2 = Toplevel(master=imgShowApp)
			btnOKTmp = tk.Button(master=self.miniWindow2, text='OK', command=self.noNameRenameWarning)
			btnOKTmp.grid(row=2, column=0, sticky=tk.W, columnspan=1)

		self.miniWindow2.title("No Name Warning")
		self.miniWindow2.attributes('-topmost', True)

		labelMultiInfoTmp = tk.Label(master=self.miniWindow2, text=strWarning)
		labelMultiInfoTmp.grid(row=0, column=0, sticky=tk.W, columnspan=1)

	# End of createWarningDialog(self, strWarning, mMaster) function.




	"""
	cambiarNombre(self) callback function is used mainly to get the new file 
	name from the user, and to call another function member of a different 
	class. This other function actually does the file rename process.
	"""
	def cambiarNombre(self):
		# print('Function  -  cambiarNombre() - callback')

		# Checking that new file name has more than zero characters.
		if len(self.entry.get()) > 0:
			# Invoking a control class member function to actually rename the
			# file.
			rnmSucced, newRnmdPath = self.cntrlClass.cambiarNombreCntrl(self.index, self.entry.get())
			# Checking the rename process succed or failed.
			if rnmSucced:
				#Updating the GUI Label file info with the new file name.
				self.txtFileInfo.set('FN: ' + newRnmdPath)	
				self.miniWindow.destroy()
			else:
				# Warning the user about possible OS errors.
				# Creating the warning message.
				newRnmdPath = newRnmdPath + '\nA file already exist with that filename.' 
				self.createWarningDialog(newRnmdPath, 2)

		else:
			# Warning user about that the new file name cannot be empty.
			self.createWarningDialog('Field name cannot be empty. Enter new name or click calcel btn.', 2)

	# End of cambiarNombre(self) function.




	"""
	noNameRenameWarning(self) callback function is used just to destroy a 
	warnig dialog window. 
	NOTE: Ther are almost equal functions because todavia no hayo como mandar 
	parametros a una callback function.

	"""
	def noNameRenameWarning(self):
		# print('Function  -  noNameRenameWarning(self)')

		self.miniWindow2.destroy()

	# End of noNameRenameWarning(self) function




	"""
	noNameRenameWarningX(self) callback function is used just to destroy a 
	warnig dialog window. 
	"""
	def noNameRenameWarningX(self):
		# print('Function  -  noNameRenameWarningX(self)')

		self.miniWindow2.destroy()

	# End of noNameRenameWarningX(self) function




	"""
	cambiarMultiNombres(self) callback function is used mainly to build the 
	rename multiple files window.
	"""
	def cambiarMultiNombres(self):
		# Function  -  cambiarMultiNombres(self)')

		if self.playingStatus == True:
			print("To rename a picture set the app on Paused Mode.")
		else:
			if len(self.entry.get()) > 0:
				self.miniWin = Toplevel(master=self.miniWindow)
				self.miniWin.title(" - miniWin - Multi-Renaming Image Files")
				self.miniWin.attributes("-topmost", True)
			
				self.MultiInfoTmpLbl = tk.Label(master=self.miniWin, text='To rename multiple files click on the image to add it to the list of files to be renamed.\nClick OK button to enter multi-rename mode or cancel to end this process.')
				self.MultiInfoTmpLbl.grid(row=0, column=0, sticky=tk.W, columnspan=4)

				self.OKTmpBtn = tk.Button(master=self.miniWin, text='OK', command=self.enterRenameMultiFilesMode)
				self.OKTmpBtn.grid(row=2, column=0, sticky=tk.W, columnspan=1)

				self.SelectImgBtn = tk.Button(master=self.miniWin, text='Select Img', state='disable', command=self.selectImageToRename)
				self.SelectImgBtn.grid(row=2, column=1, sticky=tk.W, columnspan=1)

				self.DoneSelectingBtn = tk.Button(master=self.miniWin, text='Done', state='disable',  command=self.askIfRenameIsOK)
				self.DoneSelectingBtn.grid(row=2, column=2, sticky=tk.W, columnspan=1)

				CancelBtn = tk.Button(master=self.miniWin, text='Cancel', command=self.cancelMultiNombres)
				CancelBtn.grid(row=2, column=3, sticky=tk.W, columnspan=1)
			else:
				self.miniWinNoFNWarning = Toplevel(master=self.miniWindow)
				self.miniWinNoFNWarning.title('Enter New File Name.')
				self.miniWinNoFNWarning.attributes('-topmost', True)

				lblNFNWarning = Label(master=self.miniWinNoFNWarning, text='Enter New File Name To Continue')
				lblNFNWarning.grid(row=0, column=0, sticky=tk.W, columnspan=2)

				btnOK = Button(master=self.miniWinNoFNWarning, text='OK', command=self.noFileNameWarning)
				btnOK.grid(row=1, column=0, sticky=tk.W, columnspan=1)

	# End of cambiarNombre(self) function.
	



	"""
	noFileNameWarning(self) function is used to destroy the dialog warning 
	created to let user know that a new file name has to be entered in order 
	to continue with the renaming process.
	"""
	def noFileNameWarning(self):
		#print('Function  -  noFileNameWarning(self)')

		# Destroying the dialog warning window.
		self.miniWindow.destroy()

	# End of noFileNameWarning(self) function.




	"""
	enterRenameMultiFilesMode(self) function is used to enable and disable some
	button widgets, and to pass and set some variables on a different class.
    It pass the new filename that are going to be used during the multi files 
	renaming process. 
	"""
	def enterRenameMultiFilesMode(self):
		# print('Function  -  enterRenameMultiFilesMode(self)')

		self.enableDisableBtns()
		# Passing the new filename.
		self.cntrlClass.setPicNameCtrl(self.picName.get())

	# End of enterRenameMultiFilesMode(self) function.




	"""
	selectImageToRename(self) function is used to get all the image files that
	are going to be renamed. This function calls another function memeber of a 
	different class to set in a dictionary all the selected file names. This 
	function pass the index of the file path list to the other function. This 
	index 
	"""
	def selectImageToRename(self):
		# print("Function  -  selectImageToRename()")

		# Checking the index is not out of range.
		# Creo que esta parte if del if-else block nunca es accedida ya que el 
		# diccionario nunca recive alguna insercion en este modulo de la app.
		# Toda insercion se hace en el modulo de control.
	###########################################################################
	# En 11/1/2021 se elimino el if block del if-else block.
	# Solo checar que surgan errores por la eliinacion de este bloque de codigo.
	# Checarlo el funcionamiento antes de borrar el codigo eliminado.
	###########################################################################
	#	if self.index in self.pathFileDict:
			# This file has been selected already.
	#		print('Ese archivo ya existe en la lista de files.')
	#	else:
		# Checking if the selected file has been inserted into the dictionary.
		if self.cntrlClass.selectImageToRenameCntrl(self.index):
			# Creo que esta variable no se usa en nigna otra parte del program,
			#self.similarNames.append()
			pass
		# The selected image was not included to be reanmed.
		else:
			# OS error during the file insertion into the dictionary.
			print('Some error paso durante la agrupacion de image names')


	# End of selectImageToRename(self) function.




	"""
	enableDisableBtns(self) function is used to change the text and color of 
	some widget on the app main window. This action is to let user know that 
	the app is in multi-renaming mode.
	"""
	def enableDisableBtns(self):
		# print('Function  -  enableDisableBtns(self)')

		# if block to set widget in normal mode.
		if self.appMultiRenameMode == True:
			self.miniWin.destroy()
			self.appMultiRenameMode = False
			self.setDirBtn['state'] = 'normal'
			self.delayTimeSB['state'] = 'normal'
			self.renameBtn['state'] = 'normal'
			self.deleteBtn['state'] = 'normal'
		# else block to set the widgets in multi-renaming mode.
		elif self.appMultiRenameMode == False:
			imgShowApp.title(imgShowApp.titleNombre.get() + " - IS NOW IN RENAME MODE -")
			self.appMultiRenameMode = True
			self.MultiInfoTmpLbl['text'] = 'The program is now in multi-rename files MODE.'
			self.OKTmpBtn['state'] = 'disable'
			self.SelectImgBtn['state'] = 'normal'
			self.DoneSelectingBtn['state'] = 'normal'

			self.setDirBtn['state'] = 'disable'
			self.delayTimeSB['state'] = 'disable'
			self.renameBtn['state'] = 'disable'
			self.deleteBtn['state'] = 'disable'

	# End of enableDisableBtns(self) function.




	"""
	askIfRenameIsOK(self) function is used to confirm that the new filename and
	all the filenames to be rebamed are correct. All this info is entered by the
	user. 
	This function also creates a dialog to present to the user the information 
	and gather more information that are needed to procee with the renaming 
	process.
	"""
	def askIfRenameIsOK(self):
		# print('Function  -  askIfRenameIsOK(self)')

		# if block to creates a dialog when the user has not selected any 
		# filename to be renamed and click the done button.
		if self.cntrlClass.getDictionarySizeCntrl()  <= 0:
			#talvez hacer una window para avisar al usuario de este problema
			self.miniWinNoSlction = Toplevel(master=self.miniWin)
			self.miniWinNoSlction.title('No selection done')
			self.miniWinNoSlction.attributes("-topmost", True)

			lblNFNWarning = Label(master=self.miniWinNoSlction, text='You have to select at least one file to rename or cancel to stop renaming.')
			lblNFNWarning.grid(row=0, column=0, sticky=tk.W, columnspan=4)

			btnOK = Button(master=self.miniWinNoSlction, text='OK', command=self.okNoSlctnWin)
			btnOK.grid(row=1, column=0, sticky=tk.W, columnspan=1)

			cancelBtn = Button(master=self.miniWinNoSlction, text='Cancel', command=self.cancelNoSlctnWin)
			cancelBtn.grid(row=1, column=1, sticky=tk.W, columnspan=1)
		# else block to create a dialog to show user some information and to 
		# get more information needed to completed the renaming process.
		else:
			# local function list to get all filenames similar to the new 
			# filename entered by the user.
			listaXXX = []
			# local function variable to hold the similar list size.
			counter = 0
			listaXXX = self.cntrlClass.getSimilarFNListCntrl(self.picName.get())
			counter = len(listaXXX)

			# Starting-creating dialog window.
			self.miniWinAskIsOK = Toplevel(master=self.miniWin)
			self.miniWinAskIsOK.title("Is Ok To Rename Files?")
			self.miniWinAskIsOK.attributes("-topmost", True)

			similarFNamesLbl = tk.Label(master=self.miniWinAskIsOK, text='Similar File Names List.')
			similarFNamesLbl.grid(row=0, column=0, sticky=tk.W, columnspan=4)
			# Text are show the filenames similar to new filename.
			scrolFNme = scrolledtext.ScrolledText(master=self.miniWinAskIsOK, wrap=tk.WORD, width = 30, height = 8, font=("Times New Roman", 11))
			scrolFNme.grid(row=1, column=0, sticky=tk.W, columnspan=4)
			scrolFNme.insert(tk.INSERT, listaXXX)
			scrolFNme.configure(state='disable')

			numberToIncreaseLbl = tk.Label(master=self.miniWinAskIsOK, text='Enter Number To Increase To Add To File Name. ')
			numberToIncreaseLbl.grid(row=2, column=0, sticky=tk.W, columnspan=4)
			# This number will be added to the filename.
			nmbrToIncreasEntry = tk.Entry(master=self.miniWinAskIsOK, textvariable=self.numberIncrease)
			nmbrToIncreasEntry.grid(row=3, column=0, sticky=tk.W, columnspan=4)

			charSequeToAdLbl = tk.Label(master=self.miniWinAskIsOK, text='Enter Characters To Add To The File Name:')
			charSequeToAdLbl.grid(row=4, column=0, sticky=tk.W, columnspan= 4)
			# This string will be added to the filename.
			charSequeToAdEntry = tk.Entry(master=self.miniWinAskIsOK, textvariable=self.charsToAdFName)
			charSequeToAdEntry.grid(row=5, column=0, sticky=tk.W, columnspan=4)
 
			askIsOKLbl = tk.Label(master=self.miniWinAskIsOK, text='Confirm Renaming Multiple Files?\nThis action cannot be undone.\nCancel will stop all the process.')
			askIsOKLbl.grid(row=6, column=0, sticky=tk.W, columnspan=4)

			isOkBtn = tk.Button(master=self.miniWinAskIsOK, text='OK', command=self.renameMultipleFiles)
			isOkBtn.grid(row=7, column=0, sticky=tk.W, columnspan=1)

			cancelBtn = tk.Button(master=self.miniWinAskIsOK, text="Cancel", command=self.stopMultiRenameFiles)
			cancelBtn.grid(row=7, column=1, sticky=tk.W, columnspan=1)

	# End of askIfRenameIsOK(self) function.
	



	"""
	cancelMultiNombres(self) callback function is used to destroy the window 
	that start the multi rename process, and to stop that process. It also 
	clear the dictionary member of a different class used to hold the files 
	that wil be renamed.
	"""
	def cancelMultiNombres(self):
		# print('Function  -  cancelMultiNombres(self)')
		
		# Setting app title to normal name.
		imgShowApp.title(imgShowApp.titleNombre.get())
		# Clearing the variable holding the new file name.
		self.picName.set("")
		
		# Block to destroy only this window before moving tha app to the 
		# multi rename mode.
		if self.appMultiRenameMode == False:
			self.miniWin.destroy()
		# Setting app widget to no rename mode.
		elif self.appMultiRenameMode == True:
			self.enableDisableBtns()

		# Exiting the multi-files-rename mode.
		self.appMultiRenameMode = False
		# Clearing dictionary member of a different class.
		self.cntrlClass.clearSelectedImgDicCntrl()
		# Destroying the parent window of this window.
		self.miniWindow.destroy()
		
	# End of cancelMultiNombres(self) function.




	"""
	okNoSlctnWin(self) callback function is invoked when the OK button on the 
	no file selection dialog windos is clicked. This function is used only to 
	destroy the dialog that is created to let user know that at least one file 
	has to be selected in order to continue with the renaming process.
	"""
	def okNoSlctnWin(self):
		# print('Function  -  okNoSlctnWin(self)')

		self.miniWinNoSlction.destroy()

	# End of okNoSlctnWin(self) function.




	"""
	cancelNoSlctnWin(self) callback function is used to build a dialog warning
	to let user know that to proceed with the renaming process at least one file
	has to be selected and inserted into the dictionary.
	"""
	def cancelNoSlctnWin(self):
		# print('Function  -  cancelNoSlctnWin(self)')

		# Clearing the list and dictionary and the new filename.
		self.fileListToRename.clear()
		self.pathFileDict.clear()
		self.picName.set("")
		# Destroying all dialog windows created for the multi-renaming process.
		self.miniWinNoSlction.destroy()
		self.miniWin.destroy()
		self.miniWindow.destroy()
		self.enableDisableBtns()

	# End of cancelNoSlctnWin(self) function.




	"""
	renameMultipleFiles(self) callback function is invoked when the OK button 
	of the 'Is OK to Rename' window is clicked. This function will set some 
	widgets before the renaming process starts. This function will call a 
	different function to actually do the real renaming operations.
	It does not receive nor return anything
	"""
	def renameMultipleFiles(self):
		# print('Funcion  -  renameMultipleFiles()')

		# Updating some widgets text and colors.
		self.enableDisableBtns()
		counter = 0
		# Calling a external function to complete the renaming process.
		counter =  self.cntrlClass.renameMultipleFilesCntrl(self.charsToAdFName.get(), self.numberIncrease.get())
		# This is just for debugging.
		if counter > 0:
			print(str(counter) + ' image files were renamed')
		else:
			print('Algun tipo de error ocurrio......' + str(counter))

		# Exiting the multi-files-rename mode.
		self.appMultiRenameMode = False
		# Reseting to normal state some global variables.
		self.fileListToRename.clear()
		self.pathFileDict.clear()

		# Setting entry fields, populated by user, to nothing.
		self.picName.set("")
		self.numberIncrease.set("")
		self.charsToAdFName.set("")
		self.miniWindow.destroy()

	# End of renameMultipleFiles(self) function.




	"""
	stopMultiRenameFiles(self) callback function is invoked when button cancel
	is clicked on the 'Is OK to rename?' window. This is the last step to stop 
	the whole renaming process.
	"""
	def stopMultiRenameFiles(self):
		# print('Function  -  stopMultiRenameFiles(self)')

		# Destroying the 'Is OK To Rename' window.
		self.miniWinAskIsOK.destroy()
		# Celaring dictionary and list holding the files to be renamed.
		self.fileListToRename.clear()
		self.pathFileDict.clear()
		# Setting local variables to their normal state.
		self.numberIncrease.set("")
		self.charsToAdFName.set("")
		# Setting app widgets to no renamimg mode.
		self.enableDisableBtns()
		# Destroying all the dialog windows.
		self.miniWindow.destroy()
		# Clearing dictionary holding image files on another class.
		self.cntrlClass.clearSelectedImgDicCntrl()
		# Clearing the variable holding the new filename.
		self.picName.set("")
		# Exiting the multi-files-rename mode.
		self.appMultiRenameMode = False


	# End of stopMultiRenameFiles(self) function.



	
	"""
	cancelarCambiarNombre(self) callback function is invoked when the cancel 
	rename button is clicked. It is mainly used to destroy the dialog window.
	"""
	def cancelarCambiarNombre(self):
		# print('Function  -  cancelarCambiarNombre(self)')

		self.picName.set("")
		# Destroying the rename process window.
		self.miniWindow.destroy()

	# End of cancelarCambiarNombre(self) function.




	### End of the renaming multi files code.
	



	### Start of the deleting files code.

	"""
	deletePicture(self) callback function that is called when the delete 
	[<D>] button is clicked. This method call another function that is member 
    of another class, and that is the function that actually delete an image 
	file from the device. This action cannot be undone.
	"""
	def deletePicture(self):
		# print('Funcion  -  deletePicture()')

		if self.playingStatus == True:
			# Talvez poner un warnig al user.
			print("To delete a picture set the app on Paused Mode.")
		# else block to actually delete the image file.
		else:
			# Getting the image list size from the control class.
			self.imgNamesSize = self.cntrlClass.returnImgNamesLstSize()
			# Checling that index is within the list size range.
			if self.index >= 0 and self.index < self.imgNamesSize:
				# Calling the function that delete the image file.
				self.deleteSucced = self.cntrlClass.deletePictureCntrl(self.index)
				# Checking if deletion succed or failed
				if self.deleteSucced[0] and self.deleteSucced[1] > 0:
					# Getting the new image file list size.
					self.imgNamesSize = self.deleteSucced[1]
					# Moving the sliding forward or backward.
					if self.nextBackMode:
						self.nextPicture()
					else:
						self.backPicture()
				# Catching posible error during the deletion process.
				# Error thrown when the image file list is empty. It maybe that 
				# user has deleted all files.
				elif self.deleteSucced[1] == 0:
					# Setting some variables to values where the app was before
					# all the files were deleted.
					self.index = -1
					self.imgNamesSize = 0
					self.imgNames.clear()
					# Setting message warning to the user.
					self.txtFileInfo.set("No more files to delete....")
					self.labelInfo.configure(background="red")
					# Creating an image-photo to display and let the user know 
					# that there are not more files to display.
					self.createMyInitialImage("My Lord Nicky There Are Not More Images To Delete.")
					self.resizingPicture()
				# Catching the error thrown when the app is trying to delete a 
				# file that it does not exist in that directory.
				elif self.deleteSucced[1] == -1:
					# Creating the string message to show to the user.
					strWarning = 'The file that is being deleted does not exist in this directory.'
					self.createWarningDialog(strWarning, 2)
					# Updating the image file list size.
					self.imgNamesSize = self.cntrlClass.returnImgNamesLstSize()
					# Changing the next or back image.
					self.setIndex()
					self.playShowHelper()
				# OS error Catching.
				elif self.deleteSucced[1] == -2:
					# Faltaria crear un warning dialogo to the user.
					print('un OSERROR se produjo cuando se trataba de borrar file.')
			# Caching error due to index out of range.
			else:
				self.createMyInitialImage("My Lord Nicky There Are Not More Images To Delete.")
				self.resizingPicture()
	
	# End of setIndex() class function.



	### End of the deleting files code.




	"""
	setIndex(self) function is used to set the index next or back value. If the 
	sliding movement is forward the index value is increased by one. If movement 
	is backward the index value is decreased by one.
	"""
	def setIndex(self):
		# print('Function  -  setIndex(self)')

		if self.nextBackMode:
			self.index += 1
			# Checking the end of the list. If so index is set to zero.
			if self.index >= self.imgNamesSize: 
				self.index = 0
		else:
			self.index -= 1
			# Checking the beginning of the list. If so index is set to the length of 
			# the list minus one.
			if self.index < 0:
				self.index = self.imgNamesSize - 1  

	# End of setIndex() class function.




	"""
	setImgNamesLstSize(self) function is used to get image file list size. This 
	information is obtained from the controlling class. Only that class can 
	access the directory information and all the files in it.
	"""
	def setImgNamesLstSize(self):
		# print('Function  -  setImgNamesLstSize(self)')

		# Invoking an imgShowCntrl class function to get the image list size.
		self.imgNamesSize = self.cntrlClass.returnImgNamesLstSize()

	# End of setImgNamesLstSize() class function.


			

	"""
	do_exit(self, event) class callback function that is called when the 'q' 
	keyboard key is pressed. This function also deltes the resizedPic.png file. 
	This file is created by this program to do any change on this file and left
    the original file unchanged.
	"""
	def do_exit(self, event):
		# print('Function  -  do_exit(self, event)')

		# if statement to delete the temporary image created to resize the 
		# image to be displayed. This action allows to keep the original image
		# without any change.
		# Deleting this file keeps the list of files without change.
		strPath = self.getResizePath()
		if self.cntrlClass.deleteTmpImgFile(strPath):
			print('El resized file was deleted.')
		else:
			print('Algun tipo de error ocurrio cuando se borraba el file.')

		# Exiting the application
		self.quit()

	# End of do_exit() function.




	"""
	doExit(self) class callback method is used to shut down this program when 
    the X lower-left app button is clicked. This function also deltes the  
	resizedPic.png file. This file is created by this program to do any change 
	on this file and left the original file unchanged.
	"""
	def doExit(self):
		# print('Function  -  doExit(self)')

		# if statement to delete the temporary image created to resize the 
		# image to be displayed. This action allows to keep the original image
		# without any change.
		# Deleting this file keeps the list of files without change.
		strPath = self.getResizePath()
		if self.cntrlClass.deleteTmpImgFile(strPath):
			print('El resized file was deleted.')
		else:
			print('Algun tipo de error ocurrio cuando se borraba el file.')
		
		# Exiting the application
		self.quit()

	# End of doExit() function.




	"""
	getResizePath(self) function is used just to return the full file name path
    of the file that this program creates at the start. The file name is 
	'resizedPic.png.'
	"""
	def getResizePath(self):
		# print('Function  -  getResizePath(self)')

		return os.path.join( self.strPath, self.tmpFileName)

	# End of getResizePath(self) function.


# End of the main Window class. 




""" 
This class is to start the application. It does just a few main window 
configurations.
"""
class ImageShowApp(tk.Tk):
	"""docstring for ImageShowApp"""

	# ImageShowApp(tk.Tk) Class constructor.
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Setting the app main window title on a StringVar.
		self.titleNombre = tk.StringVar()
		self.titleNombre.set("Nicky Picture Show Project")
		# Setting the application name and title.
		self.title(self.titleNombre.get())

		# Position of the main window.
		self.geometry("+0+0")

		self.w = Window(self)
		# NOTE: Necesito ver si esta linia se puede usar en algo.
		# self.resizable(width=False, height=False)

		# NOTE: L a siguiente era la linea original solo que se tuvo que cambiar 
		# para acceder a la callback function cuando el boton del lado derecho en 
		# la parta alta es presioado.
		# Starting the class that does all the job.
		#Window(self).grid(sticky=(tk.E, tk.W, tk.N, tk.S))
		self.w.grid(sticky=(tk.E, tk.W, tk.N, tk.S))

		# Binding the app main window top-right X button to the clicking on 
		# the q keyboard key.
		self.protocol("WM_DELETE_WINDOW", self.on_exitTRX)

	# End of __init__(self, *args, **kwargs) function




	"""
	on_exitTRX(self) callback function is invoked when the top-right X button 
    is clicked to shut down this progrma. This function deletes an image file 
	that this program created at the start of this program. The file name is
	'resizedPic.png.'
	"""
	def on_exitTRX(self):
		# print('Function  -  on_exitTRX(self)')
		self.destroy()

		# Deleting the resizedFile when the app is closed.
		strPath = self.w.getResizePath()
		if self.w.cntrlClass.deleteTmpImgFile(strPath):
			print('El resized file was deleted.  on_exitTRX')
		else:
			print('Algun tipo de error ocurrio cuando se borraba el file. on_exitTRX')

	# End of on_exitTRX() function.

# End of ImageShowApp class.




"""
Making sure that this file is the one that is runnig as a stand along 
application.
"""
if __name__ == '__main__':
	imgShowApp = ImageShowApp()
	imgShowApp.mainloop()




################################### END OF FILE #######################################