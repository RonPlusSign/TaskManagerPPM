from django.shortcuts import render
from django.views import View


class HomepageView(View):
    template = "homepage.html"

    def get(self, request):
        return render(request, self.template)
