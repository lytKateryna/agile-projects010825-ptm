from rest_framework.routers import DefaultRouter

from projects.views.tasks import TaskViewSet


router = DefaultRouter()
router.register('', TaskViewSet, basename='tasks')
urlpatterns = [

]
urlpatterns += router.urls