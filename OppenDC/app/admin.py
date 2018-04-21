from django.contrib import admin

from .models import Client
from .models import Server
from .models import Source
from .models import Target
from .models import SourcesTargets
from .models import DeployHistory

admin.site.register(Client)
admin.site.register(Source)
admin.site.register(Target)
admin.site.register(SourcesTargets)
admin.site.register(Server)
admin.site.register(DeployHistory)