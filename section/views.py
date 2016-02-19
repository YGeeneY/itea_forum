from django.views.generic import ListView

from section.models import Section


class SectionView(ListView):
    model = Section
    context_object_name = 'sections'
    template_name = 'landing/base.html'
