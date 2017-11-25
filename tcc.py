import cv2
import numpy as np
import os
import shutil
from matplotlib import pyplot as plt
#################################################################################################

threshold = 0.96
pathTc = "..\\timecodes\\"
pathOutRec = "..\\out2\\"
pathOutRef = "..\\out1\\"
pathInRec = "..\\inp2\\"
pathInRef = "..\\inp1\\"
offset = 3
numberFramesBlue = 150
numberFramesQr = 150
numberFramesSusi = 2250
picCount = 5
##################################################################################################

count = 0

watchdog = 0

print("syncing Videos...")

def findMatch(settling, pathtimecode, pathdir):
 retval = -1
 marker = 0
 
 template = cv2.imread(pathtimecode +'conv%05d.png'%(settling),0)
 w, h = template.shape[::-1]
 list = os.listdir(pathdir)

 for file in list:
  marker = marker + 1
  img_rgb = cv2.imread(pathdir + file,0)
  img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
  res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
  loc = np.where( res >= threshold)
  if zip(*loc[::-1]):
   print("match at " + str(marker))
   retval = marker
   break
  #else:
   #print ("no match")
   
 return retval


while 1:
 count = findMatch(offset + watchdog,pathTc,pathInRec)
 
 if watchdog > 10:
  print("raw data broken, please get them again")
  break
 if count != -1:
  print(count)
  print(watchdog)
  break
 watchdog = watchdog + 1
 

 
i = 1

count = count + 2   ## hack has to be imporved

while count <= len(os.listdir(pathInRec)):
 #print(i)
 shutil.copy2(pathInRec + 'conv%04d.png'%(count), pathOutRec + 'rec%04d.png'%(i))
 count = count + picCount      #every picture is 5 times available
 i = i + 1
 if i >= ((numberFramesSusi/picCount) - offset): 
  break
 
i = 0 

while i < (len(os.listdir(pathOutRec))):
 shutil.copy2(pathInRef + 'image%04d.png'%(offset + watchdog + i), pathOutRef + 'ref%04d.png'%(i+1))
 i = i + 1
 
 
 

# print pt #gibt die gefundenen matches auf der console aus


