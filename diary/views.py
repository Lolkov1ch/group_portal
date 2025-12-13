from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Grade, Subject
from .forms import GradeForm


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        is_teacher = user.groups.filter(name="Teachers").exists()
        return user.is_staff or is_teacher

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "У вас немає доступу до щоденника викладача")
            return redirect("diary:grade_list")
        return redirect("login")


class GradeListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Grade
    template_name = "diary/grade_list.html"
    context_object_name = "grades"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        filter_keys = ['student', 'subject', 'date_from', 'date_to']
        current_filters = {key: request.GET.get(key) for key in filter_keys}
        
        if not any(current_filters.values()):
            session_filters = request.session.get("grade_filters")
            if session_filters and any(session_filters.values()):
                params = []
                for k, v in session_filters.items():
                    if v: params.append(f"{k}={v}")
                redirect_url = f"{reverse_lazy('diary:grade_list')}?{'&'.join(params)}"
                return HttpResponseRedirect(redirect_url)
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Grade.objects.select_related('student', 'subject', 'teacher').all()

        student_id = self.request.GET.get('student')
        subject_id = self.request.GET.get('subject')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        # Фільтрація
        if student_id:
            queryset = queryset.filter(student__id=student_id)
        
        if subject_id:
            queryset = queryset.filter(subject__id=subject_id)
            
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
            
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        # Збереження в сесію
        if any([student_id, subject_id, date_from, date_to]):
            self.request.session["grade_filters"] = {
                "student": student_id,
                "subject": subject_id,
                "date_from": date_from,
                "date_to": date_to,
            }
        elif "grade_filters" in self.request.session:
             if not self.request.GET: 
                 pass
             else:
                 pass 

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо списки для випадаючих списків фільтрів
        context["subjects"] = Subject.objects.all()
        context["students"] = User.objects.all()

        # Активні фільтри для відображення в формі
        context['active_student'] = self.request.GET.get('student')
        context['active_subject'] = self.request.GET.get('subject')
        context['active_date_from'] = self.request.GET.get('date_from')
        context['active_date_to'] = self.request.GET.get('date_to')
        
        return context


class GradeCreateView(LoginRequiredMixin, TeacherRequiredMixin, SuccessMessageMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = "diary/grade_form.html"
    success_url = reverse_lazy("diary:grade_list")
    success_message = "Оцінку успішно додано!"

    def form_valid(self, form):
        # Автоматично підставляємо викладача
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class GradeUpdateView(LoginRequiredMixin, TeacherRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = "diary/grade_form.html"
    success_url = reverse_lazy("diary:grade_list")
    success_message = "Оцінку успішно змінено!"


class GradeDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Grade
    template_name = "diary/grade_confirm_delete.html"
    success_url = reverse_lazy("diary:grade_list")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Оцінку успішно видалено")
        return response