from django.shortcuts import render
from .forms import PostForm
# Create your views here.
def handle_uploaded_file(f,uname):
    fpath='C:\\Users\\jasmine.wadhwania\\Desktop\\%s.csv'%(uname)
    with open(fpath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def register(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        print("before valid")
        if form.is_valid():
           print("entered")
           form = PostForm(request.POST,request.FILES)
           post = form.save(commit=False)
           uname = request.POST.get('username')
           post.username=uname
           post.password = request.POST.get('password')
           mqttuname = request.POST.get('mqttuser')
           post.mqttuser=mqttuname
           post.mqttpass = request.POST.get('mqttpass')
           post.port = request.POST.get('port', '')
           post.save()
           if 'file' in request.FILES:
             print("file entered")
             handle_uploaded_file(request.FILES['file'],uname)
           render(request, 'register.html', {'form': form})

    form = PostForm()
    return render(request, 'register.html', {'form': form})