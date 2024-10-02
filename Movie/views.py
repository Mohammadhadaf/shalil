from django.shortcuts import render, redirect
from django.http.response import HttpResponse, StreamingHttpResponse
from .forms import VideoUploadForm
import os 
from django.core.files.storage import default_storage
from django.conf import settings
from wsgiref.util import FileWrapper
import re
# Create your views here.
# def movie_play(request):
#     #return HttpResponse("salam sabaye khoobam")
#     return render(request, "movie.html")

def index(request):
    return render(request, "index.html")

def stream_video(request, video_name):
    video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_name)

    # چک کردن وجود فایل
    if not os.path.exists(video_path):
        return HttpResponse(status=404)

    # تنظیمات پایه و اندازه فایل
    file_size = os.path.getsize(video_path)
    range_header = request.META.get('HTTP_RANGE', None)

    # اگر درخواست range وجود داشته باشد
    if range_header:
        range_match = re.match(r"bytes=(\d+)-(\d+)?", range_header)
        if range_match:
            start_byte = int(range_match.group(1))
            end_byte = range_match.group(2)
            end_byte = int(end_byte) if end_byte else file_size - 1

            chunk_size = end_byte - start_byte + 1
            response = StreamingHttpResponse(
                file_iterator(video_path, start_byte, chunk_size),
                content_type="video/mp4"
            )
            response['Content-Length'] = str(chunk_size)
            response['Content-Range'] = f"bytes {start_byte}-{end_byte}/{file_size}"
            response['Accept-Ranges'] = 'bytes'
            response.status_code = 206
            return response

    # اگر درخواست range نبود
    response = StreamingHttpResponse(
        FileWrapper(open(video_path, 'rb')),
        content_type="video/mp4"
    )
    response['Content-Length'] = str(file_size)
    response['Accept-Ranges'] = 'bytes'
    return response

def file_iterator(file_path, start, length, chunk_size=8192):
    """این تابع فایل را به صورت chunked بر اساس start و length ارسال می‌کند."""
    with open(file_path, 'rb') as f:
        f.seek(start)
        bytes_remaining = length
        while bytes_remaining > 0:
            chunk = f.read(min(chunk_size, bytes_remaining))
            if not chunk:
                break
            yield chunk
            bytes_remaining -= len(chunk)



def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']
            # Define the media path where the file should be saved
            file_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_file.name)
            # Save the file
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            return redirect('video_list')  # Redirect to the list of uploaded videos
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})


def video_list(request):
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    video_files = os.listdir(video_dir)
    video_names = [video for video in video_files]  # Store only the names of the videos
    return render(request, 'video_list.html', {'videos': video_names})

def play_video(request, video_name):
    video_url = os.path.join(settings.MEDIA_URL, 'videos', video_name)
    return render(request, 'play_video.html', {'video_url': video_url, 'video_name': video_name})