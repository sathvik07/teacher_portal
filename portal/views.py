from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Student
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            logger.info(f"User '{username}' logged in successfully.")
            return redirect("home")
        else:
            logger.warning(f"Failed login attempt for username: '{username}'.")
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def logout_view(request):
    logger.info(f"User '{request.user.username}' logged out.")
    logout(request)
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("New user registered successfully.")
            return redirect("login")
        else:
            logger.warning("User registration failed due to invalid form data.")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def home_view(request):
    students = Student.objects.filter(teacher=request.user)
    logger.info(f"User '{request.user.username}' accessed the home view.")
    return render(request, "home.html", {"students": students})


@login_required
@csrf_protect
def add_student_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        subject = request.POST.get("subject")
        marks = request.POST.get("marks")

        if name and subject and marks:
            student, created = Student.objects.get_or_create(
                name=name,
                subject=subject,
                teacher=request.user,
                defaults={"marks": marks}
            )
            if not created:
                student.marks += int(marks)
                student.save()
                logger.info(f"Updated marks for student '{name}' in subject '{subject}'.")
                messages.success(request, f"Updated {name}'s marks for {subject} successfully!")
            else:
                logger.info(f"Added new student '{name}' for subject '{subject}'.")
                messages.success(request, f"Added new student: {name} for {subject} successfully!")
        else:
            logger.warning("Failed to add student due to missing fields.")
            messages.error(request, "All fields are required.")

    return redirect("home")


@login_required
def edit_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id, teacher=request.user)
    if request.method == "POST":
        name = request.POST.get("name")
        subject = request.POST.get("subject")
        marks = request.POST.get("marks")

        if name and subject and marks:
            student.name = name
            student.subject = subject
            student.marks = int(marks)
            student.save()
            logger.info(f"Edited student '{name}' with ID '{student_id}'.")
            messages.success(request, "Student updated successfully!")
        else:
            logger.warning(f"Failed to edit student with ID '{student_id}' due to missing fields.")
            messages.error(request, "All fields are required.")

    return redirect("home")


@login_required
def delete_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id, teacher=request.user)
    logger.info(f"Deleted student '{student.name}' with ID '{student_id}'.")
    student.delete()
    messages.success(request, f"Deleted {student.name} successfully.")
    return redirect("home")