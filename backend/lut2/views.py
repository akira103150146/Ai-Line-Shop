from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import UploadedImage
import base64
import json
import os
import traceback


# Create your views here.
def get_ang_khun_tek_page(request):
    return render(request, 'lut2/Ang-Khun-tek.html')

def get_chen_cheng_po_lumbermill(request):
    return render(request, 'lut2/Chen-Cheng-Po（lumbermill).html')

def get_chen_cheng_po_roundaout(request):
    return render(request, 'lut2/Chen-Cheng-Po（roundabout).html')

def get_fang_qing_mian(request):
    return render(request, 'lut2/Fang-Qing-Mian.html')


def get_upload_page(request):
    """顯示上傳頁面"""
    return render(request, 'lut2/upload.html')


@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    """處理圖片上傳
    
    支援兩種方式：
    1. 文件上傳（multipart/form-data）：使用 request.FILES
    2. Base64 上傳（application/json）：使用 request.body
    """
    try:
        # 確保 media 目錄存在
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            os.makedirs(media_root, exist_ok=True)
        
        # 確保子目錄存在
        for orientation in ['portrait', 'landscape']:
            subdir = os.path.join(media_root, 'lut2', orientation)
            if not os.path.exists(subdir):
                os.makedirs(subdir, exist_ok=True)
        
        # 方式1：處理文件上傳（推薦）
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            orientation = request.POST.get('orientation', 'portrait')
            
            # 驗證方向
            if orientation not in ['portrait', 'landscape']:
                orientation = 'portrait'
            
            # 創建模型實例並儲存文件
            uploaded_image = UploadedImage(
                orientation=orientation,
                image=image_file,
                original_filename=image_file.name
            )
            uploaded_image.save()
            
            return JsonResponse({
                'success': True,
                'message': '圖片上傳成功！',
                'id': uploaded_image.id,
                'image_url': uploaded_image.get_image_url(),
                'orientation': uploaded_image.orientation
            })
        
        # 方式2：處理 Base64 上傳
        elif request.content_type and 'application/json' in request.content_type:
            data = json.loads(request.body)
            image_base64 = data.get('image_base64', '')
            orientation = data.get('orientation', 'portrait')
            original_filename = data.get('filename', 'uploaded_image')
            
            if not image_base64:
                return JsonResponse({
                    'success': False,
                    'message': '缺少圖片資料'
                }, status=400)
            
            # 驗證方向
            if orientation not in ['portrait', 'landscape']:
                orientation = 'portrait'
            
            # 移除 base64 前綴（如果有的話）
            if ',' in image_base64:
                image_base64 = image_base64.split(',')[1]
            
            # 創建模型實例並儲存 base64
            uploaded_image = UploadedImage(
                orientation=orientation,
                image_base64=image_base64,
                original_filename=original_filename
            )
            uploaded_image.save()
            
            return JsonResponse({
                'success': True,
                'message': '圖片上傳成功！（Base64 格式）',
                'id': uploaded_image.id,
                'orientation': uploaded_image.orientation
            })
        
        else:
            return JsonResponse({
                'success': False,
                'message': '請提供圖片檔案或 Base64 資料'
            }, status=400)
            
    except Exception as e:
        # 記錄詳細錯誤信息（用於調試）
        error_trace = traceback.format_exc()
        print(f"Upload error: {str(e)}")
        print(f"Traceback: {error_trace}")
        
        return JsonResponse({
            'success': False,
            'message': f'上傳失敗：{str(e)}',
            'error_type': type(e).__name__
        }, status=500)
