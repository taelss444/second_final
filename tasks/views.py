from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate


def task_list(request):
    tasks = Task.objects.all()  # Показываем задачи только для текущего пользователя
    context = {'tasks': tasks}
    if request.user.is_authenticated:
        context['user_can_edit'] = True
    else:
        context['user_can_edit'] = False
    return render(request, 'tasks/task_list.html', context)


@login_required
def create_task(request):
    if not request.user.is_authenticated:  # Если пользователь не авторизован
        return redirect('login')  # Перенаправляем на страницу входа

    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Привязываем задачу к текущему пользователю
            task.save()
            return redirect('task_list')  # Перенаправляем на страницу задач
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.is_authenticated:  # Проверка авторизации
        task.completed = True
        task.save()

    return redirect('task_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')  # Если пользователь авторизован, редиректим на главную

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Создаём пользователя
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            return redirect('task_list')  # Перенаправляем на главную страницу
    else:
        form = CustomUserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('task_list')
            else:
                form.add_error(None, 'Неверные данные для входа')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)  # Выход из системы
    return redirect('task_list')