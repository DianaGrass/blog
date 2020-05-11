from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time


def gen_slug(s):
    # slugify - из строк генерирует слаги
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    # Человекопонятный  url, флаг db_index=True не нужен, т.к. поля
    # где unique=True индексируются автоматически
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    # db_index=True - флаг на индексацию, чтобы можно было делать
    # быстрый поиск по содержанию
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        # return '{}'.format(self.title)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def __str__(self):
        # return '{}'.format(self.title)
        return self.title


# class Tag(models.Model):
#     title = models.CharField(max_length=50)
#     slug = models.SlugField(default='t0', max_length=50,
#                             unique=False, db_index=True)
#
#     def __str__(self):
#         return '{}'.format(self.title)
