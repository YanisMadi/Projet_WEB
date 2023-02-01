from django.contrib import admin

from .models import Genome, SequenceInfo
#pour regarder dans django admin
admin.site.register(Genome)
admin.site.register(SequenceInfo)
