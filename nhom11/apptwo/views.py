from django.shortcuts import render
from apptwo.models import AccessRecord,Topic,Webpage
from . import forms
# Create your views here.
def index(request):
    """
    webpage_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records': webpage_list}
    return render(request,'index.html',context=date_dict)
    """
    return render(request,'basic_app/index.html')

def form_name_view(request):
    """
    form = forms.FormName()
    return render(request,'basic_app/form.html',{'form':form})
    """
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print('Validation success!')
            print('Name: '+form.cleaned_data['name'])
            print('Email: '+form.cleaned_data['email'])
            print('Text: '+form.cleaned_data['text'])

    return render(request,'basic_app/form.html',{'form':form})
