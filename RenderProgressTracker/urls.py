from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from RenderProgress.views import RenderBlockViewSet, RenderBlockMap

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'blocks', RenderBlockViewSet)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RenderBlockMap.as_view()),
    url(r'^api/', include(router.urls)),
)
