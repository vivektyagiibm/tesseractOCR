import pytesseract 
import cv2
import sys


# usage runOCR.py <listOfReceiptImageFiles>  <results.txt>

if len(sys.argv) !=3:
   print(" usage runOCR.py <listOfReceiptImageFiles>  <results.txt>") 
   exit()

# threhold of alphanumeric characters to detect restuarent name. 
MIN_LENGTH_NAME = 5
listReceiptsFile = sys.argv[1]
fileImageList = open(listReceiptsFile,'r')

# read the Receipt images list
imageList = fileImageList.readlines()


fileOut = open(sys.argv[2],'w')

# method to count alphanumeric characters in a recognized line
def countAlphaNumeric( textString):
  cnt = 0
  for i in range(len(textString)):
     if textString[i].isalpha():
        cnt = cnt +1
     elif textString[i].isdigit():
        cnt = cnt +1
  return cnt


for p in imageList:
   # read image
   img = cv2.imread(p.strip())
   print(p.strip())
   print('Receipt: '+p, file = fileOut)

   # perform OCR on image
   outputText = pytesseract.image_to_string(img, lang='eng')
   # split lines by newline chars
   linesReceipt = outputText.splitlines()

   # set default Restaurant name to None
   restName = None
   # this loop finds rhe first OCR line that has MIN_LENGTH_NAME or greater alphanumeric characters as the restuarant name. 
   for i in range(len(linesReceipt)):
      cnt = countAlphaNumeric( linesReceipt[i].strip())
      if (cnt >= MIN_LENGTH_NAME ):
         restName = linesReceipt[i].strip()
         break

   # set default total amount to None
   amount = None

   for i in range(len(linesReceipt)):
     #For the total amount, we search for a OCR line that has substring “total” or ‘otal’ in it but does not have ‘subtotal’ as we want to detect the total amount and not subtotal amount. We use both the substring ‘total’ and ‘otal‘ as a match as sometimes the first character is missing in the OCR output. One we have detected such a line, we extract its last word as the total amount. This is extracted as a string due to the possible presence of the currency character as well as some 1-2 minor alphabet/special character errors. If the “Total amount” line using the above rule is not successfully detected, we output a special token “UNK” i.e UNKNOWN as the total amount. 

     if ('total' in linesReceipt[i].strip().lower() or 'otal' in linesReceipt[i].strip().lower() ) and 'subtotal' not in linesReceipt[i].strip().lower():
        # This line contains the total amount which we will assume to be the last word in this line. 
        # Due to possible OCR errors the last word may not be a valid float/int number and may have some special characters in between. Therefore we will extract it as a string as the last word in this line. 
        amount = linesReceipt[i].strip().split()[-1]  

   # print the detected Restaurant name and total amount
   if (restName != None):
      print('Restaurant Name: '+restName,  file = fileOut)
   else:
      print('Restaurant Name: ' +'UNK', file = fileOut)
   if (amount != None):
      print('Total: '+amount, file = fileOut)
   else:
      print('Total: '+'UNK', file = fileOut)

