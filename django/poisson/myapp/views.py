from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2 as cv


# 메인
def main(request):
    img = cv.imread('img2.jpg', cv.IMREAD_COLOR)
    return render(request, 'myapp/main.html')

# 소개   
def intro(request):
    return render(request, 'myapp/intro.html')

# 옷고르기   
def cloth(request):
    return render(request, 'myapp/undecided.html')
    
# 카메라
def webcam(request):
	return render(request, 'myapp/webcam.html')