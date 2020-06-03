from django.db import models


class News(models.Model):
    name = models.CharField(max=200)

    def __str__(self):
        return self.name


class Article(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    title = models.CharField(max=200)
    year = models.IntegerField(max_length=4)
    description = models.TextField()

    def __str__(self):
        return self.title
