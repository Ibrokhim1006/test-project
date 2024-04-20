from django.urls import path
from course.view.category_views import CategorysView, CategroyView, CategoryCourseView
from course.view.course_views import CoursesView, CourseView
from course.view.section_views import SectionsView, SectionView, SectionCourseView
from course.view.lession_views import LessonsView, LessonView, LessonSectionView
from course.view.comment_views import CommentsView, CommentView, GradeView, CommentCourseView
from course.view.favorite_views import FavoritesView, FavoriteViews


urlpatterns = [
    path('category/', CategorysView.as_view(), name='All category admin'),
    path('category/<int:pk>/', CategroyView.as_view(), name="Category admin"),
    path('category/course/<int:pk>/', CategoryCourseView.as_view()),

    path('course/', CoursesView.as_view(), name='All course admin'),
    path('course/<int:pk>/', CourseView.as_view(), name='Course admin'),

    path('section/', SectionsView.as_view(), name='All sections admin'),
    path('section/<int:pk>/', SectionView.as_view(), name='Section admin'),
    path('section/course/<int:pk>/', SectionCourseView.as_view()),

    path('lesson/', LessonsView.as_view(), name='All Lessons admin'),
    path('lesson/<int:pk>/', LessonView.as_view(), name='Lesson admin'),
    path('lesson/section/<int:pk>/', LessonSectionView.as_view(), name='Lesson section'),

    path('grade/', GradeView.as_view()),
    path('comment/', CommentsView.as_view(), name='Comment course'),
    path('comment/<int:pk>/', CommentView.as_view(), name='Comment courese'),
    path('comment/course/<int:pk>/', CommentCourseView.as_view(), name='Comment course'),
    
    path('favorite/', FavoritesView.as_view(), name='Favorite users all'),
    path('favorite/<int:pk>/', FavoriteViews.as_view(), name='Favorite user'),


]