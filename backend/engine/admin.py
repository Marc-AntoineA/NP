from django.contrib import admin

from .models import *

# todo update the admin interface if needed (see Balneau Example)
admin.site.register(Tag)
admin.site.register(Picture)
admin.site.register(Neighbors)
