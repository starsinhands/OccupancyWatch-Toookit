from django.urls import path

from . import views

from App.views import index, configureroom, details, configureoccupants, exhibit, generate
    # get_classes  # 最后要把trying注释掉

urlpatterns = [
    path('index/',views.index, name='index'),
    #子路由
    path('first/',configureroom, name='first'),
    path('first-second/',details, name='first-second'),
    path('second/',configureoccupants, name='second'),
    path('third/',exhibit, name='third'),
    path('fourth/',generate, name='fourth')

    # ,path('get_classes/',get_classes,name='get_classes')
]