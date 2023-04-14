from django.db import models


class Category(models.Model):
    """
    This model has the following fields:
    - desc: the description of the category
    - id: the primary key
    - created_at: the date the category was created
    - updated_at: the date the category was updated
    The plural name is Categories
    """

    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name_plural = "Categories"


class Graphic(models.Model):
    """
    This model has the following fields:
    - desc: the description of the graphic
    - id: the primary key
    - category_id: foreign key to the category model
    - created_at: the date the graphic was created
    - updated_at: the date the graphic was updated
    """

    desc = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.desc
