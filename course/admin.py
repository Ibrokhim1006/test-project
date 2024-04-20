from django.contrib import admin
from course.models import (
    Category, Course, CourseSection, Lesson, CommentCourse, Favorites, Grade
)


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(Lesson)
admin.site.register(Grade)
admin.site.register(CommentCourse)
admin.site.register(Favorites)

