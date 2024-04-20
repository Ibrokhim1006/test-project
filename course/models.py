from django.db import models
from authen.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='course/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CourseSection(models.Model):
    name = models.CharField(max_length=250)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="section")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()
    video = models.FileField(upload_to='lessons/')
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CommentCourse(models.Model):
    comment = models.CharField(max_length=250, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comment')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Favorites(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
