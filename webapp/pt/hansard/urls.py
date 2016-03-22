from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'pt.hansard.views',
    url(r'import/$', 'import_speeches', name='home'),
)
