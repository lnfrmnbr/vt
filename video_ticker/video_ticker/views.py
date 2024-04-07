from django.shortcuts import render
from django.http import HttpResponse
import cv2
import numpy as np
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os

def index(request):
    return HttpResponse('Введите что-нибудь в url, используя ?text=...')

def create_video(message):
    width, height = 1920, 1080
    out = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    x, y = width, height // 2
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 30
    font_thickness = 2
    font_color = (255, 255, 255)
    for t in range(72):
        frame.fill(0)
        x -= 8*(len(message))+5
        cv2.putText(frame, message, (x, y), font, font_scale, font_color, font_thickness)
        out.write(frame)
    out.release()

def download_video(request):
    video_path = 'video.mp4'

    if os.path.exists(video_path):
        message = str(request.GET.get("text", 1))
        create_video(message)
        filename = os.path.basename(video_path)
        chunk_size = 8192
        video_file = open(video_path, 'rb')
        response = StreamingHttpResponse(FileWrapper(video_file, chunk_size), content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(video_path)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse("File not found", status=404)