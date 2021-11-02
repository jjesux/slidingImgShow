
"""
imgShowCntrl.py file is part of the imgShow proyect. It contains only one class
named imgShowCntrlClass. This class control the access to directories and files. 

"""



# Importing libraries to complete this image show project.
import glob
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os



"""
imgShowCtrl class is the class that will control the access to the directory to
access all the image files that will be displaying in the app main window. It 
will also perform all the manipulation done on these files. 
"""
class imgShowCtrlClass:


	"""
	This function is used to initialize all the variables that are used  in this 
	class.
	"""
	def __init__(self):
		# The name of this class.
		self.miNombre = 'Clase imgShowCntrlClass....'
		# Directory path selected by the user.
		self.strPath = ''
		# List holding all the image file paths.
		self.imgNames = []
		# Index to access specic file path.
		self.index = -1
		# Varaible to know if app is in paused mode or playing mode.
		self.playingStatus = False
		# Varaible to resize image.
		self.baseHeight = 650
		# Variable to know what direction the sliding swap is moving.
		self.nextBackMode = True
		# Varaible of temporary image file to resized.
		self.tmpFileName = 'resizedPic.png'
		# Reference to another class.
		self.imgShowClass = None

		# Renaming variables used to perform that operation.
		# List of image files to hold the files to be renamed.
		# NOTE: Creo que no se usa ya en esta ultima version.
		self.fileListToRename = []
		# Dictionary to group together all file paths to be renamed.
		self.pathFileDict = {}
		# Variable holds the dictionary size. It changes.
		self.dictSize = 0
		# List of file names similar to the new filename entered by user.
		self.similarNames = []
		# Variable to hold the new filename entered by user.
		self.picName = ''

	# End of __init__(self) function.

	
	
	
	### Begining of renaming process.




	"""
	selectImageToRenameCntrl(self, index) function is used to get the index of 
	the image filename that it is going to be renamed. The index parameter it 
	receives is used with the image file names list. This list is accessed 
	to get the file path using the index parameter. This file path is inserted 
	into a dictionary like {index-key, value-file path}.
	"""
	def selectImageToRenameCntrl(self, index):
		# print('Function  -  selectImageToRenameCntrl(self, index)')

		# Checking that the index is not out of range.
		if index >= 0 and index < len(self.imgNames):
			# File path not included because it is already in the dictionary.
			if index in self.pathFileDict:
				print('Ese archivo ya existe en la lista de files. CntrlMsg')
				return False
			# File path maybe inserted into the dictionary.
			else:
				# Do not insert the 'resizedPic.png' file.
				if self.imgNames[index].endswith(self.tmpFileName):
					print(self.imgNames[index] + '  was not included in DIC.')
					return False
				# Inserting the selected file path into the dictionary.
				else:
					self.pathFileDict[index] = self.imgNames[index]
					# Updating the dictionary size.
					self.dictSize = self.dictSize + 1
					return True

	# End of selectImageToRenameCntrl(self, index) function




	"""
	getSelectedImgToRename(self) function  CREO QUE ESTA FUNCION NO SE USA.
	"""
	#def getSelectedImgToRename(self):
		# print('Function  -  getSelectedImgToRename(self)')

	#	return self.pathFileDict

	# End of getSelectedImgToRename(self) function



	"""
	clearSelectedImgDic(self) function is used to clear or empty the image 
	filenames dictionary. 
	"""
	def clearSelectedImgDicCntrl(self):
		# print('Function  -  clearSelectedImgDicCntrl(self)')

		self.pathFileDict.clear()
		self.dictSize = 0

	# edn of clearSelectedImgDicCntrl(self) function




	"""
	getDictionarySize(self) function is used to return the size of the local 
	dictionary used to group together all the filenames to be renamed.
	"""
	def getDictionarySizeCntrl(self):
		# print('Function  -  getDictionarySizeCntrl(self)')

		return self.dictSize

	# End of  getDictionarySizeCntrl(self) function




	"""
	getSimilarFNList(self, picName) function is used to get all the filenames 
	in the selected directory that are similar to the new filename entered by 
	user. This will help to determine the number that will be added to the 
	filename.
	"""
	def getSimilarFNListCntrl(self, picName):
		# print('Function  -  getSimilarFNListCntrl(self, picName)')

		# for loop to traverse the whole list of filenames.
		for fN in self.imgNames:
			# Separating file path from filename.
			elPath, nombre = os.path.split(fN)
			if picName in nombre:
				# Adding similar filenames to the list.
				self.similarNames.append(nombre)
			else:
				pass

		return self.similarNames

	# End of getSimilarFNListCntrl(self, picName) function




	"""
	setPicNameCtrl(self, picName) function is used to get the new filename that 
	is going to be used to rename multiple image files.
	"""
	def setPicNameCtrl(self, picName):
		# print('Function  -  setPicNameCtrl(self, picName)')

		# Initializing a local variable to hold the new filename.
		self.picName = picName

	# End of setPicNameCtrl(self, picName) function




	"""
	renameMultipleFilesCntrl(self, charsToAdFName, numberIncrease) function is 
	used to actually rename files. This function receives two parameters. One 
	is a string of chraracters that will be added to filename. The other is a
	integer that is transformed into a string. This string will be added to the
	filename. This number wil be increased by one after each renaming process.
	This function traverses the whole dictionary to rename all files in the 
	dictionary.
	It will return the number of renamed files if not errors were thrown. It 
	will also return a negative integer if error were thrown.
	"""
	def renameMultipleFilesCntrl(self, charsToAdFName, numberIncrease):
		# print('Function  -  renameMultipleFilesCntrl(self, charsTo, numIncr)')

		counter = 0
		try:
			if len(self.picName) > 0:
				i = numberIncrease

				for k, v in self.pathFileDict.items():
					i = i + 1
					#print('iii:  ' + str(i))
					# Getting the file extension, so user does not have to 
					# type it.
					nombre, fileExte = os.path.splitext(self.imgNames[k])
					# Creating the complete new filename with the new file name
					# entered by user and some characters and a number that will
					# be increased by one.
					nombreFile = self.picName + charsToAdFName + str(numberIncrease) + fileExte
					# Building the new full file path.
					newPicName = os.path.join(self.strPath, self.picName + charsToAdFName + str(i))
					# Adding the file extension to the new filename entered by
					# user.
					newPicName = newPicName + fileExte
					# Executing the renaming operation.
					os.rename(self.imgNames[k], newPicName)
					# Updating the filename list with the new filename.
					self.imgNames[k] = newPicName
					# Increasing the varaible holding the number of renamed 
					# files.
					counter = counter + 1

				# clearing the filename dictionary after renaming all the files.
				self.pathFileDict.clear()
				# Setting local variables to their normal state.
				self.picName =''
				numberIncrease = 0 
				charsToAdFName = ''
				# Returning the number of files that were renamed.
				return counter
			
			else:
				# Returning error number to let user know about the error.
				# Error about index out of range.
				return -1
		# Catching System errors.
		except OSError as osE:
			#print('OS-OS-ERROR-ERROR: ' + osE.strerror)
			return -2

	# End of renameMultipleFilesCntrl(self, charsTo, numberIncrease) function.

	


	"""
	cambiarNombreCntrl(self, index, pathToRnm) function is used to actually 
	rename or change the filename at index define by the user.
	The parameters it receives are the index value and the filename path of the
	file the user want to rename.
	"""
	def cambiarNombreCntrl(self, index, pathToRnm):
		# print('funcion - cambiarNombreCntrl()   iSCntrl.py')
		
		try:
			# Checking that the filename entered by the user is not empty.
			if len(pathToRnm) > 0:
				# Getting the file extension, so user does not have to type.
				nombre, fileExte = os.path.splitext(self.imgNames[index])
				#Building the new full file path.
				newPicName = os.path.join(self.strPath, pathToRnm)
				# Adding file extension to the new filename entered by user.
				newPicName = newPicName + fileExte
				# Executing the renaming process.
				os.rename(self.imgNames[index], newPicName)
				# Updating the image file list with the new filename.
				self.imgNames[index] = newPicName
				# Returning True if renaming was completed. False otherwise.
				# It also returns the new filename.
				return [True, self.imgNames[index]]

		# Catching any error, if something goes wrong.
		except OSError as osE:
			print('CNTRL---OS-ERROR-ERROR: ' + osE.strerror)
			return [False, osE.strerror]


	# End of cambiarNombreCntrl(self, index, pathToRnm) function.




	### Begining of renaming process.




	"""
	doesImageExist(self, index) function is used to check if an image file 
	exist in the selected directory.
	"""
	def doesImageExist(self, index):
		return os.path.exists(self.imgNames[index])

	# End of doesImageExist(self, index) function.
		
	


	"""
	setRef(self, myClassXXX) function is used to set a local reference to 
	another class.
	"""
	def setRef(self, myClassXXX):
		self.imgShowClass = myClassXXX

	# End of setRef(self, myClassXXX) function.




	"""
	setStrPath(self, strPath) function is used to set the local class variable 
	to hold the image file path.
	"""
	def setStrPath(self, strPath):
		self.strPath = strPath

	# End of setStrPath(self, strPath) function.




	"""
	setPlayingStatus(self, status) function is used to set the local class 
	variable to know if the app is paused or playing.
	"""
	def setPlayingStatus(self, status):
		self.playingStatus = status

	# End of setPlayingStatus(self, status) function.




	"""
	showImagenCntrl(self, index) function is used to actually get the image file
    from the selected directory. It manipulate that file to actually get an 
	image file that can be displayed on a Label widget. 
	The parameter index is used to get the image path on the image file list user 
	want to display.
	It returns a list with 3 elements.
	[index, file path, photo to be displayed]
	"""
	def showImagenCntrl(self, index):
		#print('Calling:  showImagen() ** File: imgShowCntrl.py')

		# If block to get the image file path and opem it.
		if len(self.imgNames) >= 1 and index >= 0 and index < len(self.imgNames):
			# Catching any error while opening a file object.
			try:
				self.img = Image.open(self.imgNames[index])
			except IOError:
				# Handling OS errors.
				return [-1, 'It is like image file has been deleted or corrupted. Reload Files.\nTo reload files click the directory button.\nIndex ' + str(index), None]
				
			# Resizing the image to fit the main window displaying zone.
			hPercent = (self.baseHeight / float(self.img.size[1]))
			widthSized = int(float(self.img.size[0]) * float(hPercent))
			self.img = self.img.resize((widthSized, self.baseHeight), Image.ANTIALIAS)

			#Saving the temporary image with new sizes. This is the image that 
			#is displayed.
			self.img.save(self.strPath + self.tmpFileName)

			self.photo = ImageTk.PhotoImage(self.img)
			self.img.close()
			# Returning the new and resized image-photo file.
			return [index, self.imgNames[index], self.photo]

		# Debugging information, and returning error information. 
		# This error maybe about index being out of range.
		else:
			# print("Image List is empty or the index is out of range....imgShowCntrl.py")
			return [-2, 'Image List is empty or the index is out of range.', None]
			
	# End of showImagen(self) class function.



	
	### Begining of deleting process.




	"""
	deletePictureCntrl(self, index) function is used to actually delete files 
	in the directory selected by the user. The index parameter indicates which 
	file in the image files list will be delete. 
	This function try to catch any error that may happen as the result of 
	delete files. 
	This function returns a list containing only one boolean and an integer 
	value. The boolena is True if the deleting process succeed other wise is 
	False. The integer value represent the error type. These values can be 
	0, -1 and -2.
	"""
	def deletePictureCntrl(self, index):
		# Checking that image list is not empty.
		if len(self.imgNames) > 0:
			# Making sure that the picture file exist.
			if os.path.exists(self.imgNames[index]):	
				# Error catching if there is any problem deleting the picture 
				# file.
				try:
					os.remove(self.imgNames[index])
				except (IOError, OSError):
					#print("SYSTEM ERROR REMOVING FILE.")
					# Exiting the method-function without crashing the app
					return [False, -2]
			else:
				print("The indicated file does not exist on this directory.")
				print("Exiting the deleting function.")
				# Catching file does not exist error in the directory.
				# Updating the imge list to pop out all files that do not exist
				# in that directory.
				self.updateImgNamesList()
				return [False, -1]

			self.setDirectoryPath(self.strPath)
			if len(self.imgNames) == 0:
				# Exiting the function with the delete process succeeding and 
				# with the image files list empty. 
				return [True, 0]
			# Exiting the function with success and the file list not being 
			# empty.
			return [True, len(self.imgNames)]

		# Letting know user that there is not more files that can be deleted.
		else:
			# Exiting the function with deleting process failing and with the 
			# file list being empty.
			return [False, 0]

	# End of deletePicture() function.

	


	### End of deleting process.




	"""
	returnImgNamesLstSize(self) function is used to get and return the image 
	file list size.
	"""
	def returnImgNamesLstSize(self):
		return len(self.imgNames)

	# End of returnImgNamesLstSize(self) class function.

	


	"""
	setIndex(self, index) function is used to set in this class the image file 
	list index of the image user want to be displayed. It receives the index of 
	such image file path on the list.
	"""
	def setIndex(self, index):
		self.index = index

	# End of setIndex() class function.




	"""
	returnIndexUpdated(self) function is used to the index when a picture has 
	being deleted and the size of the image file list may has changed.
	"""
	def returnIndexUpdated(self):
		return self.index

	# End of returnIndexUpdated(self) function.
	



	"""
	setDirectoryPath(self, strPath) function is used to access the directory 
	pointed by the strPath parameter to get all the image files in it. It also 
	set the forward slash to backward slash for the windows system. It also 
	creates a image file path list of all the image files the directory holds.
	It returns the size of such a list.
	The strPath parameter holds the directory path.
	This function is called by its counter part on the GUI module of the app.
	"""
	def setDirectoryPath(self, strPath):
		# Setting the a function local variable with image file path.
		dirName = strPath

		#if-statement: User canceled the directory selection.
		if not dirName:
			# NOTE: It is possible that this part of the if-else block is never
			# accessed.
			# Calling this function to set the app in play mode. Directory 
			# selection was canceled.
			pass
		else:
			# Building the absolute image file paths.
			self.strPath = dirName + '/'
			# Getting only file with estension jpg, png and jpeg.
			self.imgNames = glob.glob(self.strPath + '*.jpg')
			self.imgNames = self.imgNames + glob.glob(self.strPath + '*.png')
			self.imgNames = self.imgNames + glob.glob(self.strPath + '*.jpeg')

			#for loop to change all file path separator from '\' to '/'
			for i in range(len(self.imgNames)):
				self.imgNames[i] = self.imgNames[i].replace('\\', '/')

			return len(self.imgNames)

	# End of setDirectorio(self) function.




	"""
	updateImgNamesList(self) function is used to update the image file list from
	the selected directory. This maybe necesary if some files have been deleted 
	and the size list has changed. There maybe image files on the list that do 
	not exist any more.
	So, reading the directory again resolve that issue.
	"""
	def updateImgNamesList(self):
		
		# Getting only file with estension jpg, png and jpeg.
		self.imgNames = glob.glob(self.strPath + '*.jpg')
		self.imgNames = self.imgNames + glob.glob(self.strPath + '*.png')
		self.imgNames = self.imgNames + glob.glob(self.strPath + '*.jpeg')

		#for loop to change all file path separator from '\' to '/'
		for i in range(len(self.imgNames)):
			self.imgNames[i] = self.imgNames[i].replace('\\', '/')

	# End of updateImgNamesList(self) function.


	def deleteTmpImgFile(self, tmpImgFilePath):
		try:#if os.path.exists(tmpImgFilePath):	#strPath):
			os.remove(tmpImgFilePath)#strPath)
			return True
		except OSError as ose:
			print('No se borro el resizepic file...cntrlFile')
			print("PATH: " + tmpImgeFilePath + '...cntrlFile')
			return False

################################### END OF FILE #######################################