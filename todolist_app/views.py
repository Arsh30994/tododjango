from django.shortcuts import render, redirect, get_object_or_404
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def todolist(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            if not instance.title:
                instance.title = instance.task[:200]
            instance.save()
            messages.success(request, 'New Task added!')
            return redirect('todolist')
        messages.error(request, 'Could not add task. Please try again.')
    else:
        form = TaskForm()

    all_tasks = TaskList.objects.filter(manage=request.user).order_by('-id')
    paginator = Paginator(all_tasks, 5)
    page = request.GET.get('pg')
    all_tasks = paginator.get_page(page)

    return render(request, 'todolist.html', {'all_tasks': all_tasks, 'form': form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if task.manage == request.user:
        task.delete()
        messages.success(request, 'Task deleted!')
    else:
        messages.error(request, 'Access Restricted, You are not allowed!')
    return redirect('todolist')


@login_required
def edit_task(request, task_id):
    task_obj = get_object_or_404(TaskList, pk=task_id)
    if task_obj.manage != request.user:
        messages.error(request, 'Access Restricted, You are not allowed!')
        return redirect('todolist')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task Edited!')
            return redirect('todolist')
        messages.error(request, 'Could not update task. Please try again.')
    else:
        form = TaskForm(instance=task_obj)

    return render(request, 'edit.html', {'task_obj': task_obj, 'form': form})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, 'Access Restricted, You are not allowed!')
    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = get_object_or_404(TaskList, pk=task_id)
    if task.manage == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request, 'Access Restricted, You are not allowed!')
    return redirect('todolist')


def index(request):
    context = {
        'index_text': 'welcome to Index page.',
    }
    return render(request, 'index.html', context)


@login_required
def contact(request):
    context = {
        'contact_text': 'welcome to contact page.',
    }
    return render(request, 'contact.html', context)


def about(request):
    context = {
        'about_text': 'welcome to about page.',
    }
    return render(request, 'about.html', context)
