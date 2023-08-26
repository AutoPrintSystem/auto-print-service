

from django.shortcuts import render, redirect
from .models import Order, OrderFile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

# 이건 PyMuPDF
# import fitz

# 이건 Poppler-pdfinfo
import subprocess 
import tempfile
import os

# import PyPDF2
from django.core.files.uploadedfile import InMemoryUploadedFile


### 메인페이지, 프린트 설정 페이지, 결제 페이지
def print_main(req):
    return render(req, 'print_main.html')

def get_pdf_page_count(pdf_path):
    cmd = ["C:\\Users\\Owner\\anaconda3\\Library\\bin\\pdfinfo.exe", pdf_path]
    try:
        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        for line in output.stdout.decode('utf-8').splitlines():
            if "Pages:" in line:
                return int(line.split(":")[1].strip())
        return 0
    except subprocess.CalledProcessError:
        return 0
    

def print_detail(req):
    if req.method == "GET":
        if not req.user.is_authenticated:
            return redirect('accounts:login')
        else:
            return render(req, "print_detail.html")
    elif req.method == "POST":
        files = req.FILES.getlist('files')
        color = req.POST['color']
        user_request = req.POST['request']

        print_date_str = req.POST['print_date']
        print_time_str = req.POST['print_time']

        if not files:
            messages.error(req, "파일을 선택해주세요.")
            return render(req, "print_detail.html")

        # if not pw or not pw.isdigit() or len(pw) != 4:
        #     messages.error(req, "비밀번호는 숫자 4자리를 입력해야 합니다.")
        #     return render(req, "print_detail.html")

        if not print_date_str or not print_time_str:
            messages.error(req, "프린트 날짜와 시간을 선택해주세요.")
            return render(req, "print_detail.html")
        
        total_pages = 0
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                for chunk in file.chunks():
                    tmpfile.write(chunk)
                
                total_pages += get_pdf_page_count(tmpfile.name)
        
        order_price = total_pages * 100

        print_datetime_str = f"{print_date_str} {print_time_str}"
        print_datetime = timezone.datetime.strptime(print_datetime_str, '%Y-%m-%d %H:%M')

        order = Order.objects.create(
            order_user=req.user, 
            order_price=order_price, 
            order_request=user_request,
            order_color=color,
            print_date=print_datetime
        )

        for file in files:
            OrderFile.objects.create(order=order, file=file)
        
        return redirect('payment')

def print_payment(req):
    latest_order = Order.objects.filter(order_user=req.user).order_by('-order_date').first()
    files = []
    if latest_order:
        order_files = OrderFile.objects.filter(order=latest_order)
        for order_file in order_files:
            files.append(order_file)
    context = {
        'files': files,
    }
    return render(req, 'print_payment.html', context)


### 마이페이지 & 결제내역
def print_mypage(req):
    if not req.user.is_authenticated:
        return redirect('accounts:login')
    context = {
        'user': req.user
    }
    return render(req, 'remoteprint/mypage.html', context)

def print_payment_detail(req):
    if not req.user.is_authenticated:
        return redirect('accounts:login')

    orders = Order.objects.filter(order_user=req.user).order_by('-order_date')
    orders_with_files = []
    
    for order in orders:
        order_files = OrderFile.objects.filter(order=order)
        orders_with_files.append({
            'order': order,
            'files': order_files,
        })
    
    context = {
        'orders_with_files': orders_with_files,
        'orders_count': orders.count(),
    }

    return render(req, 'remoteprint/payment_detail.html', context)

def print_cancel_order(req, order_id):
    if req.method == 'POST':
        order = Order.objects.get(id=order_id, order_user=req.user)
        current_time = timezone.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(order.print_date)
        print(formatted_time)

        order_time = datetime.strptime(order.print_date, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")

        time_difference = order_time - current_time

        # 분단위로 바꾸기 
        total_seconds = time_difference.total_seconds()

        if time_difference >= timedelta(minutes=5):
            order.delete()
            return redirect('main')
        elif time_difference < timedelta(minutes=0):
            order.delete()
            return JsonResponse({'message': '12345'}, status=400)
        else:
            return JsonResponse({'message': '123'}, status=400)
        
def print_guide(req):
    return render(req, 'guide.html')