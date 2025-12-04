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
    return render(request, 'lut2/upload_random.html')

def get_gallery_page(request):
    """顯示畫廊頁面，從資料庫載入上傳圖片"""
    images = []
    # 取出所有圖片，最新的在前
    uploaded_images = UploadedImage.objects.order_by('-created_at')
    
    for item in uploaded_images:
        image_url = item.get_image_url()
        
        if not image_url:
            continue
        
        # 處理詩詞顯示：如果沒有儲存詩詞，使用預設文字
        comment = item.poem_content
        if not comment:
            comment = "捕捉到了決定性的瞬間！大師級作品。"
        else:
            # 簡單處理：移除（節錄）字樣，讓畫廊顯示乾淨一點
            comment = comment.replace("（節錄）", "")

        images.append({
            "url": image_url,
            "type": item.orientation or 'portrait',
            "id": f"KAGI-{item.id:04d}",
            # 將儲存的詩詞資訊傳給前端
            "comment": comment, 
            "title": item.poem_title or "",
            "author": item.poem_author or ""
        })
    
    # 確保 images_json 總是有效的 JSON 字符串
    images_json = json.dumps(images, ensure_ascii=False)
    
    context = {
        "images_json": images_json,
        "has_images": len(images) > 0
    }
    return render(request, 'lut2/gallery.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    """處理圖片上傳 (包含隨機詩詞儲存)"""
    try:
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            os.makedirs(media_root, exist_ok=True)
        
        for orientation in ['portrait', 'landscape']:
            subdir = os.path.join(media_root, 'lut2', orientation)
            if not os.path.exists(subdir):
                os.makedirs(subdir, exist_ok=True)
        
        # 僅支援處理文件上傳
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            orientation = request.POST.get('orientation', 'portrait')
            
            # --- 接收前端傳來的隨機詩詞 ---
            poem_title = request.POST.get('poem_title', '')
            poem_author = request.POST.get('poem_author', '')
            poem_content = request.POST.get('poem_content', '')
            # ---------------------------

            # 驗證
            MAX_FILE_SIZE = 10 * 1024 * 1024
            if image_file.size > MAX_FILE_SIZE:
                return JsonResponse({'success': False, 'message': '文件太大'}, status=400)
            
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if image_file.content_type not in allowed_types:
                return JsonResponse({'success': False, 'message': '不支援的格式'}, status=400)
            
            if orientation not in ['portrait', 'landscape']:
                orientation = 'portrait'
            
            # 創建並儲存 (包含詩詞)
            uploaded_image = UploadedImage(
                orientation=orientation,
                image=image_file,
                original_filename=image_file.name,
                poem_title=poem_title,
                poem_author=poem_author,
                poem_content=poem_content
            )
            uploaded_image.save()
            
            return JsonResponse({
                'success': True,
                'message': '上傳成功！',
                'id': uploaded_image.id,
                'image_url': uploaded_image.get_image_url(),
                'poem_title': uploaded_image.poem_title 
            })
        
        else:
            return JsonResponse({'success': False, 'message': '請提供圖片檔案'}, status=400)
            
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Upload error: {str(e)}")
        print(f"Traceback: {error_trace}")
        return JsonResponse({
            'success': False,
            'message': f'上傳失敗：{str(e)}'
        }, status=500)

def get_gallery_data(request):
    """
    API: 回傳畫廊資料 (JSON 格式)，供前端定時更新使用
    """
    images = []
    # 取出所有圖片，最新的在前
    uploaded_images = UploadedImage.objects.order_by('-created_at')
    
    for item in uploaded_images:
        image_url = item.get_image_url()
        
        if not image_url:
            continue
        
        # 處理詩詞顯示
        comment = item.poem_content
        if not comment:
            comment = "捕捉到了決定性的瞬間！大師級作品。"
        else:
            comment = comment.replace("（節錄）", "")

        images.append({
            "url": image_url,
            "type": item.orientation or 'portrait',
            "id": f"KAGI-{item.id:04d}",
            "comment": comment, 
            "title": item.poem_title or "",
            "author": item.poem_author or ""
        })
    
    return JsonResponse({
        "images": images,
        "count": len(images)
    })