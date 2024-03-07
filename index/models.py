from django.db import models


# Create your models here.

class SinaResou(models.Model):
    title = models.CharField(max_length=255)
    hot_value = models.IntegerField(default=0)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.title


class Company(models.Model):
    company = models.CharField(max_length=255, primary_key=True)


class Brand(models.Model):
    brand = models.CharField(max_length=255, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='brands')


class Flashnews(models.Model):
    title = models.TextField()
    content = models.TextField(default=None)
    url = models.URLField(max_length=255)
    pic_url = models.URLField(max_length=255)
    ptime = models.DateTimeField(auto_now_add=False)
    user_id = models.BigIntegerField(default=None)
    user_name = models.CharField(max_length=255)
    user_verified = models.CharField(max_length=255)
    related_car = models.CharField(max_length=255)
    avatar_url = models.URLField(max_length=255)
    post_platform = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class LongNews(models.Model):
    title = models.TextField(default=None)
    content = models.TextField(default=None)
    summary = models.TextField(default=None)
    url = models.URLField(max_length=255)
    ptime = models.DateTimeField(auto_now_add=False)
    post_platform = models.CharField(max_length=255)
    platform_avatar = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class HeaderData(models.Model):
    company = models.CharField(max_length=255)
    market_segmentation = models.CharField(max_length=255, default='全部')
    car = models.CharField(max_length=255, default='全部')
    sale = models.IntegerField(default=None)
    share = models.FloatField(default=None)
    w2w = models.FloatField(default=None)
    wow = models.FloatField(default=None)
    year = models.IntegerField(default=None)
    week = models.IntegerField(default=None)
    area = models.CharField(max_length=255, default=None)


class Cars(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cars')
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    car = models.CharField(max_length=255, primary_key=True)
    length = models.IntegerField(default=None)
    width = models.IntegerField(default=None)
    height = models.IntegerField(default=None)
    car_type = models.CharField(max_length=255, default=None)
    car_class = models.CharField(max_length=255, default=None)
    car_body_form = models.CharField(max_length=255, default=None)
    price_interval = models.CharField(max_length=255, default=None)


class PromotionInfo(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='promotion_info')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='promotion_info')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='promotion_info')
    promotion = models.TextField(default=None)
    price = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    source = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    area = models.CharField(max_length=255, default=None)
    summary = models.TextField()


class GtmInfo(models.Model):
    car_id = models.IntegerField(default=None)
    car_name = models.CharField(max_length=255, default=None)
    pic_url = models.URLField(max_length=255, default=None)
    price = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=255)
    update_time = models.DateTimeField()
    sell_status = models.CharField(max_length=255, default=None)
    car_url = models.URLField(max_length=255, default=None)


class CompanySales(models.Model):
    # 企业销量数据
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_sales')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='company_sales')
    sale = models.IntegerField(default=None)
    mom = models.FloatField(default=None)
    m2m = models.FloatField(default=None)
    month = models.IntegerField(default=None)
    year = models.IntegerField(default=None)
    year_sale = models.IntegerField(default=None)
    category = models.CharField(max_length=255, default=None)


class PcautoCars(models.Model):
    car_id = models.IntegerField(default=None)
    car_name = models.CharField(max_length=255, default=None)
    pic_url = models.URLField(max_length=255, default=None)
    price = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=255)
    update_time = models.DateTimeField()
    sell_status = models.CharField(max_length=255, default=None)
    car_url = models.URLField(max_length=255, default=None)
    car_class = models.CharField(max_length=255, default="未知")
    company = models.CharField(max_length=255, default="未知")
    brand = models.CharField(max_length=255, default="未知")


class UserInfo(models.Model):
    user_name = models.CharField(verbose_name="用户名", max_length=16, unique=True)
    phone = models.BigIntegerField(verbose_name="手机号", unique=True)
    email = models.EmailField(verbose_name="邮箱", unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
