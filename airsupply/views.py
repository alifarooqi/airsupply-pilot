from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item


class BrowseView(generic.ListView):
    template_name = 'clinic-manager/browse.html'
    context_object_name = 'all_items'

    def get_queryset(self):
        return Item.objects.all()

