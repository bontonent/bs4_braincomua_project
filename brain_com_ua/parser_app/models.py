from django.db import models

class Product(models.Model):
     product_id = models.CharField(max_length=200, unique=True)
     product_name = models.CharField(max_length=100, null=True, blank=True)
     color = models.CharField(max_length=25, null=True, blank=True)
     memory = models.CharField(max_length=25, null=True, blank=True)
     brand = models.CharField(max_length=50, null=True, blank=True)
     price = models.IntegerField(null=True, blank=True)
     dis_price = models.IntegerField(null=True, blank=True)
     photo = models.CharField(max_length=500, null=True, blank=True) # maybe error
     prodcut_code = models.CharField(max_length=25, null=True, blank=True)
     count_feadback = models.IntegerField(null=True, blank=True)
     display_diagonal = models.CharField(max_length=25, null=True, blank=True)
     display_resolution = models.CharField(max_length=25, null=True, blank=True)
     dict_charact = models.JSONField(null=True, blank=True)

     #[1] Полное название товара
     #[2] Цвет
     #[3] Объем памяти
     #[4] Производитель
     #[5] Цена обычная
     #[6] Цена акционная (если есть)
     #[7] Все фото товара. Здесь нужно собрать ссылки на фото и сохранить в список
     #[8] Код товара
     #[9] Кол-во отзывов
     #[10] Диагональ экрана
     #[11] Разрешение дисплея
     #[12] Характеристики товара. Все характеристики на вкладке. Характеристики собрать как словарь
  
     def __str__(self):
          return f"Name: {self.name}."
