from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, blank=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class ConferenceRank(models.Model):
    title = models.CharField(max_length=20, blank=False)
    name = models.CharField(max_length=200, blank=True, default=None)
    rank = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Conference Rank"
        verbose_name_plural = "Conference Ranks"

    def __str__(self):
        return self.title


class PaperDetail(models.Model):
    title = models.CharField(max_length=200, blank=False)
    url = models.URLField(blank=False, unique=True)
    published_year = models.IntegerField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    conference = models.ForeignKey(ConferenceRank, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "PaperDetail"
        verbose_name_plural = "PaperDetails"

    def __str__(self):
        return self.title
