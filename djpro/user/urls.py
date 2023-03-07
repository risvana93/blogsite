from django.urls import path
from .views import *

urlpatterns = [
   path('uhome/',UserHome.as_view(),name="uhome"),
   path('profile/',ViewProfile.as_view(),name="prof"),
   path('addbio/',UserProView.as_view(),name="addbio"),
   path('chpsw/',changePasswordView.as_view(),name="chpassword"),
   path('updatebio/<int:user_id>',UpdateBioView.as_view(),name="updatebio"),
   path('addcmnt/<int:id>',add_comment,name="add-cmnt"),
   path('addlike/like<int:bid>',add_like,name='add-like'),
   path('myblogs',MyBlogView.as_view(),name='my-blogs')
]