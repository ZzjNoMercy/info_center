import json

from django.core.exceptions import ValidationError
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, reverse, redirect
from django.utils import timezone
from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from .models import (SinaResou, Flashnews, LongNews, HeaderData, PromotionInfo, GtmInfo, CompanySales, PcautoCars,
                     UserInfo)
from .utils import BootstrapForm, md5


# Create your views here.
# noinspection PyUnresolvedReferences


def home(request):
    sina_resous = SinaResou.objects.all()[0:10]
    flashnews = Flashnews.objects.all().order_by('-ptime')
    longnews = LongNews.objects.all().order_by('-ptime')[0:20]
    header_data_gsev = HeaderData.objects.filter(Q(market_segmentation='A0+A00 2门纯电') & Q(week=8) & Q(year=2024))[0]
    header_data_binguo = HeaderData.objects.filter(Q(car='五菱缤果') & Q(week=8) & Q(year=2024))[0]
    header_data_xingguang = HeaderData.objects.filter(Q(car='五菱星光') & Q(week=8) & Q(year=2024))[0]
    promotion_infos = PromotionInfo.objects.filter(Q(end_time__gte=timezone.now()))
    gtm_infos = GtmInfo.objects.filter(
        Q(update_time__month=timezone.now().month) & Q(update_time__year=timezone.now().year)
    )
    return render(request, 'index.html', {'sina_resous': sina_resous, 'flashnews': flashnews,
                                          'longnews': longnews, "header_data_gsev": header_data_gsev,
                                          "header_data_binguo": header_data_binguo,
                                          "header_data_xingguang": header_data_xingguang,
                                          "promotion_infos": promotion_infos, "gtm_infos": gtm_infos})


def demo(request):
    return render(request, 'demo.html')


def search(request):
    q = request.GET.get('q')
    # if q:
    longnews = LongNews.objects.filter(title__contains=q).order_by('-ptime')
    flashnews = Flashnews.objects.filter(Q(title__contains=q) | Q(user_verified__contains=q)).order_by('-ptime')
    promotion_infos = PromotionInfo.objects.filter(
        (Q(brand_id__brand__contains=q) | Q(company_id__company__contains=q)) & Q(end_time__gte=timezone.now())
    ).order_by('end_time')
    car_infos = PcautoCars.objects.filter(
        (Q(brand__contains=q) | Q(company__contains=q) | Q(car_name__contains=q)) & ~Q(car_class="") & Q(
            sell_status='在售')).order_by(
        '-update_time')
    length = {
        'longnews_len': len(longnews),
        'flashnews_len': len(flashnews),
        'promotion_infos_len': len(promotion_infos),
        'car_infos_len': len(car_infos),
        'infos_len': len(longnews) + len(flashnews) + len(promotion_infos) + len(car_infos)
    }
    if length['infos_len'] != 0:
        return render(request, 'search_results.html', context={
            'longnews': longnews, "q": q, 'length': length, 'flashnews': flashnews, 'promotion_infos': promotion_infos,
            'car_infos': car_infos
        })
    else:
        return render(request, "blank.html")


def rank(request):
    company_sales = {
        "1月": CompanySales.objects.filter(month=1).order_by("-sale"),
        "2月": CompanySales.objects.filter(month=2).order_by("-sale")
    }
    for query_set in company_sales.values():
        # 求出每个月销量第一
        max_sale = 0
        for company_sale in query_set:
            if company_sale.sale > max_sale:
                max_sale = company_sale.sale
        # 计算百分比
        for company_sale in query_set:
            company_sale.percent = '{:.2%}'.format(company_sale.sale / max_sale)
    return render(request, "rank.html", context={"company_sales": company_sales})


def longnews_ajax(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        q = request.POST.get("q")
        longnews = LongNews.objects.filter(title__contains=q).order_by('-ptime')
        datas = serializers.serialize("json", longnews)
        return JsonResponse(json.loads(datas), safe=False)
    else:
        return redirect(reverse('index:home'))


def flashnews_ajax(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        q = request.POST.get("q")
        flashnews = Flashnews.objects.filter(
            ~Q(user_name="") & (Q(title__contains=q) | Q(user_verified__contains=q))).order_by('-ptime')
        datas = serializers.serialize("json", flashnews)
        return JsonResponse(json.loads(datas), safe=False)
    else:
        return redirect(reverse('index:home'))


def promotion_infos_ajax(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        q = request.POST.get("q")
        promotion_infos = PromotionInfo.objects.filter(
            (Q(brand_id__brand__contains=q) | Q(company_id__company__contains=q)) & Q(end_time__gte=timezone.now())
        ).order_by('end_time')
        datas = serializers.serialize("json", promotion_infos)
        return JsonResponse(json.loads(datas), safe=False)
    else:
        return redirect(reverse('index:home'))


def car_infos_ajax(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        q = request.POST.get("q")
        car_infos = PcautoCars.objects.filter(
            (Q(brand__contains=q) | Q(company__contains=q) | Q(car_name__contains=q)) & ~Q(car_class="") & Q(
                sell_status='在售')).order_by('-update_time')
        datas = serializers.serialize("json", car_infos)
        return JsonResponse(json.loads(datas), safe=False)
    else:
        return redirect(reverse('index:home'))


class LoginForm(BootstrapForm.BootStrapUserForm):
    phone = forms.CharField(label="手机号", required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5.md5(pwd)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            int(phone)
            return int(phone)
        except ValueError:
            raise ValidationError('请输入正确的手机号')


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', context={"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_obj = UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_obj:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', context={"form": form})
        request.session['info'] = user_obj.user_name
        return redirect(reverse('index:home'), context={"user_obj": user_obj})


class UserModelForm(BootstrapForm.BootStrapUserModelForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))
    phone = PhoneNumberField()

    class Meta:
        model = UserInfo
        fields = ['user_name', 'phone', 'email', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5.md5(password)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5.md5(confirm) != pwd:
            raise ValidationError('两次输入密码不一致')
        return md5.md5(confirm)

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(str(phone)) != 11:
            raise forms.ValidationError("请输入11位手机号码")
        return phone


def sign(request):
    # 添加用户
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'sign_up.html', context={"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect(reverse('index:login'))
    return render(request, 'sign_up.html', context={"form": form})


def logout(request):
    request.session.clear()
    return redirect(reverse('index:login'))