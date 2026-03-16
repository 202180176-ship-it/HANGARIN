from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm # Import the form you defined above
from django.core.paginator import Paginator


@login_required
def task_list(request):
    # 1. Start with tasks for the logged-in user
    tasks_list = Task.objects.filter(user=request.user).order_by('-created_at')
    
    # 2. Get search/filter parameters
    search_query = request.GET.get('q')
    status_filter = request.GET.get('status')
    
    # 3. Apply filters
    if search_query:
        tasks_list = tasks_list.filter(title__icontains=search_query)
    if status_filter:
        tasks_list = tasks_list.filter(status=status_filter)
        
    # 4. Paginate
    paginator = Paginator(tasks_list, 6)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)
    
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # 1. Don't save yet! Create the object in memory
            new_task = form.save(commit=False)
            
            # 2. Manually attach the current user
            new_task.user = request.user
            
            # 3. Now save to the database
            new_task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

def complete_task(request, pk):
    # 1. Find the task in the database
    task = get_object_or_404(Task, pk=pk)
    
    # 2. Change the status or a 'completed' boolean field
    task.completed = True  # Assuming you have a boolean field
    task.status = "Completed" # Or update your status field
    task.save()
    
    # 3. Send the user back to the task list
    return redirect('task_list') # Replace 'task_list' with your URL name

def delete_task(request, pk):
    # 1. Find the task
    task = get_object_or_404(Task, pk=pk)
    
    # 2. Delete it from the database
    task.delete()
    
    # 3. Redirect back to the task list
    return redirect('task_list')

def dashboard(request):
    all_tasks = Task.objects.all()
    context = {
        'total': all_tasks.count(),
        'completed': all_tasks.filter(status='Completed').count(),
        'pending': all_tasks.filter(status='Pending').count(),
        'urgent': all_tasks.filter(priority__name='High', status='Pending')[:5],
    }
    return render(request, 'dashboard.html', context)
