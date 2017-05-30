from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2 as cv
import numpy as np
from os.path import abspath, join, dirname
from django.template import loader, Context
from django import forms
import base64 
import os
import matplotlib.pyplot as plt
from os import listdir



'''
컬러별 HSV값
red - 2 95 81
peach - 9 44 96
light brown - 24 31 67
dark brown - 26 89 25
brown - 26 90 45

orange - 36 92 94
khaki - 46 83 23
gold - 48 89 81
yellow - 50 92 98
olive - 52 39 83

gray - 0 0 60
light green - 69 54 92
green - 145 53 61
mint - 184 9 94
skyblue - 187 32 87

blue green - 193 83 52
navy - 225 80 40
blue - 235 82 54
lavender - 285 21 78
purple - 293 66 55

pink - 324 36 100
red violet - 327 89 74
light pink - 333 20 94
dark red - 348 78 50
black - 0 0 0

cream - 0 0 94
white - 0 0 100
'''


HsvArray = [(2, 95, 81),(9, 44, 96),(24, 31, 67),(26, 89, 25),(26, 90, 45),
         (36, 92, 94),(46, 83, 23),(48, 89, 81),(50, 92, 98),(52, 39, 83),
         (0, 0, 60),(69, 54, 92),(145, 53, 61),(184, 9, 94),(187, 32, 87),
         (193, 83, 52),(225, 80, 40),(235, 82, 54),(285, 21, 78),(293, 66, 55),
         (324, 36, 100),(327, 89, 74),(333, 20, 94),(348, 78, 50),(0, 0, 5),
         (0, 0, 94),(0, 0, 100)]

# rawData = '10,20,30,40,50,60,70,80,90,100,110,120'
# HsvArray[0][2] 이런 식으로 접근

look1 = False
look2 = False
isDenim = False

# 메인
def main(request):
    return render(request, 'myapp/main.html')

# 소개   
def intro(request):
   return render(request, 'myapp/intro.html')

# 옷고르기   
def cloth(request):
   if request.method == 'POST':
      selectSet = KeywordForm(request.POST)

      if request.POST.get("show"):
        selectSet = request.POST.get("show")
        specialText = selectSet.split(',')

        top_bottom = False 
        outer_bottom = False
        onepiece = False


        # 상의 / 하의 / 아우터 / 원피스 / 색1 / 색2
        # 0  /  1  /  2   /  3   /  4  / 5 
         
        if(specialText[0]!='null'): # 상의 + 하의
          top_bottom = True
          topName = specialText[0]
          topColor = specialText[4]
          btmColor = specialText[5]
          if(topName == 't shirt'):
            topName = 'T-shirt'
          elif(topName =='long sleeved t shirt'):
            topName = 'long sleeved T-shirt'
          btmName = specialText[1]
          if(btmName =='a line skirt'):
            btmName = 'A line skirt'
          elif(btmName =='h line skirt'):
            btmName = 'H line skirt'
          elif(btmName == 'blue jeans'): # 청바지 -> jeans 폴더 내에 blue jeans로 있음
            btmName = 'jeans'
            btmColor = 'blue'
          elif(btmName == 'denim skirt'):
            btmColor ='blue'


        if(specialText[2]!='null'): # 하의 + 아우터
          outer_bottom = True
          outerName = specialText[2]
          btmName = specialText[1]
          outerColor = specialText[4]
          btmColor = specialText[5]
          if(btmName =='a line skirt'):
            btmName = 'A line skirt'
          elif(btmName =='h line skirt'):
            btmName = 'H line skirt'
          elif(btmName == 'blue jeans'): # 청바지 -> jeans 폴더 내에 blue jeans로 있음
            btmName = 'jeans'
            btmColor = 'blue'
          elif(btmName == 'denim skirt'):
            btmColor ='blue'
          elif(outerName == 'denim jacket'):
            outerColor = 'blue'

        if(specialText[3]!='null'): # 원피스
          onepiece = True
          onepieceName = specialText[3]
          onepieceColor = specialText[4]

        #path = 'C:\\ColorHarmony\\Cloth'
        #folderList = listdir(path) # 폴더 이름 리스트

        savePath = 'C:\\code\\170526_ver2\\poisson\\myapp\\static\\myapp\\img\\result\\' # 이미지 저장 절대경로
        #C:\Users\user\Desktop\170524_ver3\poisson\myapp
        resultImgPath = 'myapp/img/result/' # html에서 사용할 static 경로
        imgNum = 0
        resultImgUrl =[0 for _ in range(1000)] # 0으로 초기화

        #searchText_TopBottom = topColor+' '+topName+' '+btmColor+' '+btmName
        #searchText_OuterBottom = outerColor+' '+outerName+' '+btmColor+' '+btmName

        if(top_bottom):
          searchText_TopBottom = topColor+' '+topName+' '+btmColor+' '+btmName
          path = 'C:\\ColorHarmony\\Cloth\\'+topName +'_'+ btmName
          imgList = listdir(path) # 그 폴더 내 이미지들 검사

          for imgUrl in imgList: # 각 이미지들
            #print (imgUrl)
            #print (topColor+' '+topName+' '+btmColor+' '+btmName)
            if searchText_TopBottom in imgUrl:
              resultUrl = path+'\\'+imgUrl
              print("결과 이미지 url :", resultUrl)
              imgNum += 1
              if imgNum >5:
                break
              resultImg = cv.imread(resultUrl, cv.IMREAD_COLOR) # 이미지 읽기
              cv.imwrite(str(savePath) + 'result%d.png' % imgNum,resultImg) #결과 이미지 저장
              resultImgUrl[imgNum] =str(resultImgPath) + 'result'+ str(imgNum) +'.png' # html에 넘겨줄 경로 
              print("html에 넘겨줄 경로",resultImgUrl[imgNum])


        if(outer_bottom):
          searchText_OuterBottom = outerColor+' '+outerName+' '+btmColor+' '+btmName
          path = 'C:\\ColorHarmony\\Cloth\\'+ outerName +'_'+ btmName
          imgList = listdir(path) # 그 폴더 내 이미지들 검사

          for imgUrl in imgList: # 각 이미지들
            if searchText_OuterBottom in imgUrl:
                resultUrl = path+'\\'+imgUrl
                print("결과 이미지 url :", resultUrl)
                imgNum += 1
                if imgNum >5:
                  break
                resultImg = cv.imread(resultUrl, cv.IMREAD_COLOR) # 이미지 읽기
                cv.imwrite(str(savePath) + 'result%d.png' % imgNum,resultImg) #결과 이미지 저장
                resultImgUrl[imgNum] =str(resultImgPath) + 'result'+ str(imgNum) +'.png' # html에 넘겨줄 경로 

        if(onepiece): 
          path = 'C:\\ColorHarmony\\Cloth\\' + onepieceName
          imgList = listdir(path) # 그 폴더 내 이미지들 검사
          
          for imgUrl in imgList: # 각 이미지들
            if onepieceColor+' '+onepieceName in imgUrl:
                resultUrl = path+'\\'+imgUrl
                print("결과 이미지 url :", resultUrl)
                imgNum += 1
                if imgNum >5:
                  break
                resultImg = cv.imread(resultUrl, cv.IMREAD_COLOR) # 이미지 읽기
                cv.imwrite(str(savePath) + 'result%d.png' % imgNum,resultImg) #결과 이미지 저장
                resultImgUrl[imgNum] =str(resultImgPath) + 'result'+ str(imgNum) +'.png' # html에 넘겨줄 경로 
                print(resultImgUrl[imgNum]) 

        
        block = {'result': selectSet, 
                'result1': resultImgUrl[1],
                'result2': resultImgUrl[2],
                'result3': resultImgUrl[3],
                'result4': resultImgUrl[4],
                'result5': resultImgUrl[5],
                }
      
        return render(request, 'myapp/undecided.html', block)
   return render(request, 'myapp/undecided.html')


class KeywordForm(forms.Form):
   keywordSet = forms.CharField(label='keyword set', max_length=100) 


class KeywordForm(forms.Form):
   keywordSet = forms.CharField(label='keyword set', max_length=100) 

# 카메라
def webcam(request):
   if request.method == 'POST':
      btnColor = ButtonForm(request.POST)
      if request.POST.get("pink,black"): 
         colors = request.POST.get("pink,black") # 받아온 버튼 value
         btnColor = colors.split(',') # btnColor[0], btnColor[1]로 상하의 색상값 접근 가능   
         colorChange(btnColor[0], btnColor[1]) # 컬러 변환 모듈 실행
         return render(request, 'myapp/webcam.html', {'btnColor': btnColor})
      
      elif request.POST.get("color_set"):
         btnColor = request.POST.get("color_set")
         btnColor = btnColor.split(',')
         base64Img = request.POST.get("upload")

         if rawDataCheck(base64Img, 10): # rawData가 제대로 넘어왔을 경우
            base64Decode(base64Img) # 디코드 후 로컬 경로에 이미지 저장
            colorChange(btnColor[0], btnColor[1], base64Img) # 컬러 변환 모듈 실행. 파라미터는 split한 값 넣어줘야 함
            imageDataURL = 'C:\ColorHarmony/result.jpg'
            resultImgURL = getBase64Encode(imageDataURL)
            block = {'btnColor': btnColor, 'resultImgURL': resultImgURL}
            return render(request, 'myapp/webcam.html', block)
         else: # rawData가 제대로 구성X인 경우
            popUpCheck = 1
            block = {'popUpCheck' : popUpCheck }
            return render(request, 'myapp/webcam.html', block)
   else:
      btnColor = 'not posted'

   return render(request, 'myapp/webcam.html', {'btnColor': btnColor})


# 이름 주고받기 테스트
class NameForm(forms.Form):
   your_name = forms.CharField(label='Your name', max_length=100)

class ButtonForm(forms.Form):
   btnName = forms.CharField(label='Button name', max_length=100)

def rawDataCheck(rawData, elementNum): # rawData에 들어가야하는 요소=10개 
   rawData = rawData.split(',')
   if(elementNum == len(rawData)):
      return True
   else:
      return False

def makeTopMask(rgbImg, btmMask, nonGreenMask): # img는 hsv img
   h, w, _ = rgbImg.shape # 이미지의 높이, 너비 받아오기
   binaryMask = nonGreenMask - btmMask
   return binaryMask

def makeBtmMask(rgbImg, r, g, b, nonGreenMask):
   h, w, _ = rgbImg.shape # 이미지의 높이, 너비 받아오기
   binaryMask = np.full((h, w), 0, np.uint8) # 검은 바탕 이미지 배열  

   for i in range(w-1,0,-1): # 위쪽에서부터 채우기
        for j in range(h-1,0,-1):
           if abs(rgbImg[j,i,0]-r)<=10 and abs(rgbImg[j,i,1]-g)<=10 and abs(rgbImg[j,i,2]-b)<=10: #녹색 선을 만나면 멈추기 
              break             
           elif nonGreenMask[j,i]==255:
              binaryMask[j,i] = 255   

   return binaryMask
   

def selectColor(color):
   colorIdx = 0
   if color == 'red':
      colorIdx = 0
   elif color == 'peach':
      colorIdx = 1
   elif color == 'lightbrown':
      colorIdx = 2
   elif color == 'darkbrown':
      colorIdx = 3
   elif color == 'brown':
      colorIdx = 4
   elif color == 'orange':
      colorIdx = 5
   elif color == 'khaki':
      colorIdx = 6
   elif color == 'gold':
      colorIdx = 7
   elif color == 'yellow':
      colorIdx = 8
   elif color == 'olive':
      colorIdx = 9
   elif color == 'gray':
      colorIdx = 10
   elif color == 'lightgreen':
      colorIdx = 11
   elif color == 'green':
      colorIdx = 12
   elif color == 'mint':
      colorIdx = 13
   elif color == 'skyblue':
      colorIdx = 14
   elif color == 'bluegreen':
      colorIdx = 15
   elif color == 'navy':
      colorIdx = 16
   elif color == 'blue':
      colorIdx = 17
   elif color == 'lavender':
      colorIdx = 18
   elif color == 'purple':
      colorIdx = 19
   elif color == 'pink':
      colorIdx = 20
   elif color == 'redviolet':
      colorIdx = 21
   elif color == 'lightpink':
      colorIdx = 22
   elif color == 'darkred':
      colorIdx = 23
   elif color == 'black':
      colorIdx = 24
   elif color == 'cream':
      colorIdx = 25
   elif color == 'white':
      colorIdx = 26

   return colorIdx

# 변환할 색상이 넘어오면 해당 색으로 바꿈
def colorChange(topColor, btmColor, rawData):
   maskImg = cv.imread('C:\ColorHarmony/forMask.jpg', cv.IMREAD_COLOR) # 이미지 읽기
   resultImg = cv.imread('C:\ColorHarmony/forResult.jpg', cv.IMREAD_COLOR)
   rgbImg = resultImg.copy()
   resultImg = cv.cvtColor(resultImg, cv.COLOR_BGR2HSV)

   h, w, ch = resultImg.shape # 높이, 너비, 채널 

   path = 'C:\ColorHarmony/'
   #####################
   nonGreenMask = getNonGreenMask(resultImg)
   btmMask = np.zeros((h,w), np.uint8)
   btmMask = makeBtmMask(maskImg, 0,128,0, nonGreenMask)
   cv.imwrite(str(path) + 'btmMask.jpg', btmMask)
   topMask = np.zeros((h,w), np.uint8)
   topMask = makeTopMask(maskImg, btmMask, nonGreenMask)
   cv.imwrite(str(path) + 'topMask.jpg', topMask)

   ######################
   f = open('C:\ColorHarmony/' + "test.txt", 'w')
   f.write(rawData)
   f.close()

   # 상하의 rgb값 얻기
   topRgb = getTopRGB(rawData)
   btmRgb = getBtmRGB(rawData)
   print("base :", topRgb, btmRgb)
   userTopHue = hueCal(topRgb[0],topRgb[1],topRgb[2]) # hue 계산
   userTopVal = valCal(topRgb[0],topRgb[1],topRgb[2]) # value 계산
   userBtmHue = hueCal(btmRgb[0],btmRgb[1],btmRgb[2])
   userBtmVal = valCal(btmRgb[0],btmRgb[1],btmRgb[2]) 

   darkVal = 80

   # hue와 value값 초기
   hue = 0
   saturation = 0
   value = 0

   # 컬러 배열에서의 인덱스. 빨강부터 차례대로 0,1,2...
   topColorIdx = selectColor(topColor)
   btmColorIdx = selectColor(btmColor)

   # 선택된 버튼의 hsv값 계산
   topHue = int(HsvArray[topColorIdx][0]/2)
   topSaturation = int(0.8*HsvArray[topColorIdx][1]/100*255)
   topValue = int(0.8*HsvArray[topColorIdx][2]/100*255)

   btmHue = int(HsvArray[btmColorIdx][0]/2)
   btmSaturation = int(0.8*HsvArray[btmColorIdx][1]/100*255)
   btmValue = int(0.8*HsvArray[btmColorIdx][2]/100*255)

   topValDistance = topValue - userTopVal
   btmValDistance = btmValue - userBtmVal

   whiteMask = getWhiteMask(resultImg)
   # 컬러 체인지
   for i in range(h):
    for j in range(w):
        if topMask[i,j] == 255 and userTopVal>200 and whiteMask[i,j] == 255:
            resultImg = adjustColorValue(resultImg, topHue, topSaturation*0.8, topValDistance*0.2, i, j)        
        elif topMask[i,j] == 255 and (userTopHue-10<= resultImg[i,j,0]<= userTopHue+10):            
            resultImg = adjustColorValue(resultImg, topHue, topSaturation, topValDistance, i, j)
        elif topMask[i,j] == 255 and resultImg[i,j,2] <= darkVal: # 어두운 색일 경우
            resultImg = adjustColorValue(resultImg, topHue, topSaturation, topValDistance, i, j)
        elif topMask[i,j] == 255 and isAchromatic(rgbImg[i,j,0],rgbImg[i,j,1],rgbImg[i,j,2]):
            resultImg = adjustColorValue(resultImg, topHue, topSaturation, topValDistance, i, j)         
        #####################################################################
        if btmMask[i,j] == 255 and (userBtmHue-10<=resultImg[i,j,0]<= userBtmHue+10): 
            resultImg = adjustColorValue(resultImg, btmHue, btmSaturation, btmValDistance, i, j)
        elif btmMask[i,j] == 255 and resultImg[i,j,2] <= darkVal: # 어두운 색일 경우
            resultImg = adjustColorValue(resultImg, btmHue, btmSaturation, btmValDistance, i, j)  
        elif btmMask[i,j] == 255 and isAchromatic(rgbImg[i,j,0],rgbImg[i,j,1],rgbImg[i,j,2]):
            resultImg = adjustColorValue(resultImg, btmHue, btmSaturation, btmValDistance, i, j)
        #if i == 150 and j == 150:
        # print("현재 밝기", resultImg[i,j,2])
        # print("검정, 유저색", btmValue, userBtmVal)
        # print("거리", btmValDistance)

   resultImg = cv.cvtColor(resultImg, cv.COLOR_HSV2BGR)

   cv.imwrite(str(path) + 'result.jpg', resultImg)


def adjustColorValue(resultImg, hue, sat, vDistance, i, j):
   resultImg[i,j,0] = hue # H
   resultImg[i,j,1] = sat # S
   if resultImg[i,j,2] + vDistance >= 255: # 밝기 범위 초과 방지
      resultImg[i,j,2] = 255
   elif resultImg[i,j,2] + vDistance <= 0: # 밝기 범위 초과 방지
      resultImg[i,j,2] = 0
   else:
      resultImg[i,j,2] += vDistance

   return resultImg

def isAchromatic(r, g, b):
   np.seterr(over='ignore')
   r_g = abs(r-g)
   r_b = abs(r-b)
   g_b = abs(g-b)

   if r_g<=25 and r_b<=25 and g_b<=25:
      return True
   else:
      return False

def getWhiteMask(img):
   # define range of white color in HSV
   sensitivity = 60
   lower_white = np.array([0,0,255-sensitivity])
   upper_white = np.array([255,sensitivity,255])
   # Threshold the HSV image to get only white colors
   mask = cv.inRange(img, lower_white, upper_white)

   return mask

def getNonGreenMask(img):
   # define range of green color in HSV
   sensitivity = 35
   lower_green = np.array([60 - sensitivity, 100, 0])
   upper_green = np.array([60 + sensitivity, 255, 255])
   # Threshold the HSV image to get only white colors
   mask = cv.inRange(img, lower_green, upper_green)
   mask = 255 - mask

   path = 'C:\ColorHarmony/'
   cv.imwrite(path + 'nonGreenMask.jpg',mask)

   return mask

# (결과)이미지 base64 encode  
def getBase64Encode(imageDataURL):
   encodedImg = 'data:image/jpg;base64,'
   data = base64.b64encode(open(imageDataURL, "rb").read())
   data = data.decode('utf-8')
   encodedImg += data
   return encodedImg

# base64 decode 후 이미지 저장
def base64Decode(rawData):
   rawData = rawData.split(',') # data:image/png;base64, 의 뒷부분이 이미지 데이터임.
   data1 = rawData[1]
   data1 = base64.b64decode(data1) # 디코드
   data1 = bytearray(data1)
   data1 = np.asarray(data1, dtype = "uint8") # 이미지로 변환
   data1 = cv.imdecode(data1, cv.IMREAD_COLOR)

   data2 = rawData[3]
   data2 = base64.b64decode(data2) # 디코드
   data2 = bytearray(data2)
   data2 = np.asarray(data2, dtype = "uint8") # 이미지로 변환
   data2 = cv.imdecode(data2, cv.IMREAD_COLOR)

   path = 'C:\ColorHarmony/' # 이미지 저장 경로
   cv.imwrite(str(path) + 'forResult.jpg', data1)
   cv.imwrite(str(path) + 'forMask.jpg', data2)

# RGB 컬러모델에서 HSV 컬러모델 값으로 변환
def getHSV(rawData):
   rawData = rawData.split(',')
   r = int(rawData[4])
   g = int(rawData[5])
   b = int(rawData[6])
   userTopHue = hueCal(r,g,b) # hue 계산
   userTopVal = valCal(r,g,b) # value 계산

   r = int(rawData[7])
   g = int(rawData[8])
   b = int(rawData[9])
   userBtmHue = hueCal(r,g,b)
   userBtmVal = valCal(r,g,b)


# 유저 상의 RGB값
def getTopRGB(rawData):
   rawData = rawData.split(',')

   r = int(rawData[4])
   g = int(rawData[5])
   b = int(rawData[6])
   rgbList = [r,g,b]

   return rgbList

# 유저 하의 RGB값
def getBtmRGB(rawData):
   rawData = rawData.split(',')

   r = int(rawData[7])
   g = int(rawData[8])
   b = int(rawData[9])
   rgbList = [r,g,b]

   return rgbList

# 명도값 계산
def valCal(r,g,b):
   val = int(((r+g+b)/6)/100*255)

   return val

# Hue값 계산
def hueCal(red, green, blue):
   min_ = min(min(red, green), blue)
   max_ = max(max(red, green), blue)

   hue = 0.0
   if (max_ == red) :
      if((max_- min_)):
         hue = (green - blue) / (max_ - min_)
   elif(max_ == green) :
      if((max_-min_)):
         hue = 2.0 + (blue - red) / (max_ - min_)
   else :
      if((max_-min_)):
         hue = 4.0 + (red - green) / (max_ - min_)   

   hue = hue * 60
   if (hue < 0):
     hue = hue + 360

   return round(hue)/2

def makeUrlImages(path):
    urlImages = []
    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)
        for file in files:
            filepath = os.path.join(rootpath,file)
            urlImages.append(filepath)
    return urlImages

def loadImages(path):
    # return array of images

    imagesList = listdir(path)
    loadedImages = []
    for image in imagesList:
        img = cv.imread(path+'\\'+image)
        if not img is None:
          loadedImages.append(img)

    return loadedImages

def detection(img, look1, look2, isDenim, isTopDenim, isBottomDenim, top_color, bottom_color, num):
    face_cascade = cv.CascadeClassifier('C:\\ColorHarmony\\haarcascade_frontalface_default.xml')

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    height = img.shape[0]  # 전체 이미지의 높이
    width = img.shape[1]  # 전체 이미지의 너비

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:  # 얼굴 추출
        if (height > 9.5 * h + y):
            print(img.shape)
            print('face', x, y, w, h)
            print(int(x - 0.8 * w),int(x + 1.8 * w))
            if x - 0.8 * w>0:
              topImg = img[int(y + h):int(y + 4 * h), int(x - 0.8 * w):int(x + 1.8 * w)]  # 상의 이미지 생성
              downImg = img[int(y + 4 * h):int(y + 9.5 * h), int(x - 0.8 * w):int(x + 1.8 * w)]  # 하의 이미지 생성

              # topImg_hsv = cv.cvtColor(topImg, cv.COLOR_BGR2HSV)
              # downImg_hsv = cv.cvtColor(downImg, cv.COLOR_BGR2HSV)

              topImgHeight = topImg.shape[0]
              topImgWidth = topImg.shape[1]
              downImgHeight = downImg.shape[0]
              downImgWidth = downImg.shape[1]

              print('topImgWidth', topImgWidth)

              topColorImg = topImg[int(topImgHeight * 7 / 16):int(topImgHeight * 9 / 16),
                            int(topImgWidth * 7 / 16):int(topImgWidth * 9 / 16)]  # 상의 이미지에서 색 추출할 범위 이미지
              downColorImg = downImg[int(downImgHeight * 3 / 32):int(downImgHeight * 5 / 32),
                             int(downImgWidth * 1 / 8):int(downImgWidth * 7 / 8)]  # 하의 이미지에서 색 추출할 범위 이미지

              # Threshold the HSV image to get only white colors

              # topImg_hsv = cv.cvtColor(topImg, cv.COLOR_BGR2HSV)
              print(topColorImg.shape)
              topColorImg_hsv = cv.cvtColor(topColorImg, cv.COLOR_BGR2HSV)
              downColorImg_hsv = cv.cvtColor(downColorImg, cv.COLOR_BGR2HSV)
              # topImg_hsv[:,:,1:3] = 255
              #tmp_top_img = cv.cvtColor(topColorImg_hsv, cv.COLOR_HSV2RGB)  # 상의 이미지
              #tmp_bottom_img = cv.cvtColor(downColorImg_hsv, cv.COLOR_HSV2RGB) # 하의 이미지

              black_sensitivity = 100
              white_sensitivity = 40
              lowerWhite = np.array([0, 0, 255 - white_sensitivity], dtype=np.uint8)
              upperWhite = np.array([255, white_sensitivity, 255], dtype=np.uint8)
              lowerBlack = np.array([0, 0, 0], dtype=np.uint8)
              upperBlack = np.array([180, black_sensitivity, 100], dtype=np.uint8)
              
              # Threshold the HSV image to get only white colors
              # print(topColorImg_hsv)
              # print(lowerWhite)
              # print(upperWhite)

              top_mask_hsv_white = cv.inRange(topColorImg_hsv, lowerWhite, upperWhite)
              top_mask_hsv_black = cv.inRange(topColorImg_hsv, lowerBlack, upperBlack)
              bottom_mask_hsv_white = cv.inRange(downColorImg_hsv, lowerWhite, upperWhite)
              bottom_mask_hsv_black = cv.inRange(downColorImg_hsv, lowerBlack, upperBlack)
              
              topIsBlack = 0
              bottomIsBlack = 0
              topIsWhite = 0
              bottomIsWhite = 0
              topColorless = False
              bottomColorless = False
              
              topWhiteMaskHeight = top_mask_hsv_white.shape[0]
              bottomWhiteMaskHeight = bottom_mask_hsv_white.shape[0]
              topWhiteMaskWidth = top_mask_hsv_white.shape[1]
              bottomWhiteMaskWidth = bottom_mask_hsv_white.shape[1]
              topWhiteArea = topWhiteMaskHeight * topWhiteMaskWidth
              bottomWhiteArea = bottomWhiteMaskHeight * bottomWhiteMaskWidth
              
              topBlackMaskHeight = top_mask_hsv_black.shape[0]
              bottomBlackMaskHeight = bottom_mask_hsv_black.shape[0]
              topBlackMaskWidth = top_mask_hsv_black.shape[1]
              bottomBlackMaskWidth = bottom_mask_hsv_black.shape[1]
              topBlackArea = topBlackMaskHeight * topBlackMaskWidth
              bottomBlackArea = bottomWhiteMaskHeight * bottomWhiteMaskWidth

              for i in range(topWhiteMaskHeight):
                  for j in range(topWhiteMaskWidth):
                      if (top_mask_hsv_white[i][j] == 255):
                          topIsWhite += 1
                  
              for i in range(topBlackMaskHeight):
                  for j in range(topBlackMaskWidth):
                      if (top_mask_hsv_black[i][j] == 255):
                          topIsBlack += 1
                          
              for i in range(bottomWhiteMaskHeight):
                  for j in range(bottomWhiteMaskWidth):
                      if (bottom_mask_hsv_white[i][j] == 255):
                          bottomIsWhite += 1
                          
              for i in range(bottomBlackMaskHeight):
                  for j in range(bottomBlackMaskWidth):
                      if (bottom_mask_hsv_black[i][j] == 255):
                          bottomIsBlack += 1
                          

              top_histo = cv.calcHist([topColorImg_hsv], [0], None, [180], [0, 180])  # 상의 이미지
              bottom_histo = cv.calcHist([downColorImg_hsv],[0],None,[180],[0,180]) # 하의 이미지
              
              top_histo = top_histo.reshape(top_histo.shape[0])
              bottom_histo = bottom_histo.reshape(bottom_histo.shape[0])
              top_hue = np.argmax(top_histo)  # hue값 추출
              bottom_hue = np.argmax(bottom_histo)
              
              TopHistoResultColor = top_hue*2  # 결과 hue값
              BottomHistoResultColor = bottom_hue*2  # 결과 hue값
              print('top_hue', top_hue)
              print('bottom_hue', bottom_hue)
              top_hmax = max(top_histo)
              bottom_hmax = max(bottom_histo)
              # define range of white color in HSV
              top_result_color = ''
              bottom_result_color = ''
              
              if topIsBlack > topBlackArea * 1 / 4:
                  topColorless = True
                  top_result_color = 'black'
                  
              if topIsWhite > topWhiteArea * 3 / 4:
                  topColorless = True
                  top_result_color = 'white'
              
              if 1<=TopHistoResultColor<15 and not topColorless: # 색 추출
                  top_result_color = 'red'
              elif 15<=TopHistoResultColor<45 and not topColorless:
                  top_result_color = 'orange'
              elif 45<=TopHistoResultColor<75 and not topColorless:
                  top_result_color = 'yellow'
              elif 75<=TopHistoResultColor<175 and not topColorless:
                  top_result_color = 'green'
              elif 175<=TopHistoResultColor<255 and not topColorless:
                  top_result_color = 'blue'
              elif 255<=TopHistoResultColor<285 and not topColorless:
                  top_result_color = 'purple'
              elif 285<=TopHistoResultColor<315 and not topColorless:
                  top_result_color = 'pink'
              elif 315<=TopHistoResultColor<360 and not topColorless:
                  top_result_color = 'red'                
                  
              if bottomIsBlack > bottomBlackArea * 1 / 4:
                  bottomColorless = True
                  bottom_result_color = 'black'
                  
              if bottomIsWhite > bottomWhiteArea * 3 / 4:
                  bottomColorless = True
                  bottom_result_color = 'white'
              
              if 1<=BottomHistoResultColor<15 and not bottomColorless: # 색 추출
                  bottom_result_color = 'red'
              elif 15<=BottomHistoResultColor<45 and not bottomColorless:
                  bottom_result_color = 'orange'
              elif 45<=BottomHistoResultColor<75 and not bottomColorless :
                  bottom_result_color = 'yellow'
              elif 75<=BottomHistoResultColor<175 and not bottomColorless :
                  bottom_result_color = 'green'
              elif 175<=BottomHistoResultColor<255 and not bottomColorless :
                  bottom_result_color = 'blue'
              elif 255<=BottomHistoResultColor<285 and not bottomColorless :
                  bottom_result_color = 'purple'
              elif 285<=BottomHistoResultColor<315 and not bottomColorless :
                  bottom_result_color = 'pink'
              elif 315<=BottomHistoResultColor<360 and not bottomColorless :
                  bottom_result_color = 'red'
              topOk = False
              bottomOk = False 

              print('top_color', top_result_color)
              print('bottom_color', bottom_result_color)             
              # 결과값 판단            
              if(look1): # 상의 + 하의 또는 아우터 + 하의
                  if (not isDenim): # 데님 키워드가 없는 경우
                      if(top_color == top_result_color):
                          #print("TOP : TRUE")
                          topOk = True
                      else:
                          #print("TOP : FALSE")
                          topOk = False
                          
                      if(bottom_color == bottom_result_color):
                          #print("BOTTOM : TRUE")
                          bottomOk = True
                      else:
                          #print("BOTTOM : FALSE")
                          bottomOk = False
                  elif (isDenim): # 데님 키워드가 있는 경우
                      if(isTopDenim and not isBottomDenim): # 청자켓의 경우
                          if('blue' == top_result_color):
                              #print("TOP : TRUE")
                              topOk = True
                          else:
                              #print("TOP : FALSE")
                              topOk = False
                              
                          if(bottom_color == bottom_result_color):
                              #print("BOTTOM : TRUE")
                              bottomOk = True
                          else:
                              #print("BOTTOM : FALSE")
                              bottomOk = False
                      if(isBottomDenim and not isTopDenim): # 청바지, 청치마의 경우
                          if(top_color == top_result_color):
                              #print("TOP : TRUE")
                              topOk = True
                          else:
                              #print("TOP : FALSE")
                              topOk = False
                              
                          if('blue' == bottom_result_color):
                              #print("BOTTOM : TRUE")
                              bottomOk = True
                          else:
                              #print("BOTTOM : FALSE")
                              bottomOk = False
                      if(isTopDenim and isBottomDenim): # 청 + 청 패션인 경우
                          if('blue' == top_result_color):
                              #print("TOP : TRUE")
                              topOk = True
                          else:
                              #print("TOP : FALSE")
                              topOk = False
                          if('blue' == bottom_result_color):
                              #print("BOTTOM : TRUE")
                              bottomOk = True
                          else:
                              #print("BOTTOM : FALSE")
                              bottomOk = False
                          
              elif(look2): # 원피스 
                 if(top_color == top_result_color):
                    #print("TOP : TRUE")
                    topOk = True
                 else:
                    #print("TOP : FALSE")
                    topOk = False

              cv.imwrite('C:\\ColorHarmony\\bottomImages\\result%d.png' % num,downImg)
              cv.imwrite('C:\\ColorHarmony\\topImages\\result%d.png' % num, topImg)

              #cv.imwrite('C:\\ColorHarmony\\imageResult\\result%d.png' % num, img)

              if topOk and bottomOk:
                  print("판별한 색상이 맞습니다.")
                  cv.imwrite('C:\\ColorHarmony\\imageResult\\result%d.png' % num, img)
                  return img
              else:
                  print("판별한 색상이 다릅니다.")
                  return 'Wrong'

          





