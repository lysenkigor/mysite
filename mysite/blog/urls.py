from django.urls import path

from blog import views

urlspatterns = [
    # path('', views.post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('', views.PostList.as_view(), name='post_list'),
    path('forms/', views.form_page),
    # path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:post_id>/<int:parent_comment_id>/add-dependent-comment/', views.add_dependent_comment, name='add_dependent_comment' ),
    path('<int:post_id>/<int:comment_id>/delete-comment/', views.delete_comment, name='delete_comment'),
    path('<int:post_id>/<int:comment_id>/update-comment/', views.update_comment, name='update_comment'),
]
