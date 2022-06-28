from cats.models import *
from django.db.models import Count

menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'New Article', 'url_name': 'add_page'},
        {'title': 'Contact', 'url_name': 'contact'},
        ]

class DataMixin:
    paginate_by = 3
    def get_user_context(self,**kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('cats'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        # context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

