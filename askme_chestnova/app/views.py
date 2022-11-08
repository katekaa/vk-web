PYTHONPATH="D:\vk_ed\vk-web\askme_chestnova\venv\lib\site-packages"


from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def question(request, question_id: int ):
    return render(request, 'question.html')

