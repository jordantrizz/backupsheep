from django.conf.urls import include
from django.urls import path


def _optional_include(module_path):
    try:
        return include(module_path)
    except (ImportError, ModuleNotFoundError):
        return None

app_name = "v1"

callback_urls = _optional_include('apps.api.v1.callback.urls')
incoming_urls = _optional_include('apps.api.v1.incoming.urls')

urlpatterns = [
    path(r'v1/', include([
        path(r'', include('apps.api.v1.auth.urls')),
        path(r'', include('apps.api.v1.member.urls')),
        path(r'', include('apps.api.v1.check.urls')),
        path(r'', include('apps.api.v1.log.urls')),
        path(r'', include('apps.api.v1.connection.urls')),
        path(r'', include('apps.api.v1.node.urls')),
        path(r'', include('apps.api.v1.cloud.urls')),
        path(r'', include('apps.api.v1.saas.urls')),
        path(r'', include('apps.api.v1.volume.urls')),
        path(r'', include('apps.api.v1.database.urls')),
        path(r'', include('apps.api.v1.website.urls')),
        path(r'', include('apps.api.v1.storage.urls')),
        path(r'', include('apps.api.v1.backup.urls')),
        path(r'', include('apps.api.v1.schedule.urls')),
        path(r'', include('apps.api.v1.account.urls')),
        path(r'', include('apps.api.v1.group.urls')),
        path(r'', include('apps.api.v1.invite.urls')),
        path(r'', include('apps.api.v1.notification.urls')),
        path(r'', include('apps.api.v1.utils.urls')),
        *((path(r'', callback_urls),) if callback_urls else ()),
        *((path(r'', incoming_urls),) if incoming_urls else ()),
    ])),
]
