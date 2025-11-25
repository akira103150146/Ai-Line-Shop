from django.shortcuts import render

# Create your views here.
def get_ang_khun_tek_page(request):
    return render(request, 'lut2/Ang-Khun-tek.html')

def get_chen_cheng_po_lumbermill(request):
    return render(request, 'lut2/Chen-Cheng-Po（lumbermill).html')

def get_chen_cheng_po_roundaout(request):
    return render(request, 'lut2/Chen-Cheng-Po（roundabout).html')

def get_fang_qing_mian(request):
    return render(request, 'lut2/Fang-Qing-Mian.html')
