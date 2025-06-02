from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Student
from django.urls import reverse

# Create your tests here.

class StudentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teacher', password='pass123')
        self.student = Student.objects.create(
            name="Alice", subject="Math", marks=95, teacher=self.user
        )

    def test_login_required_redirects(self):
        response = self.client.get(reverse('home'))
        expected_url = f"{reverse('login')}?next={reverse('home')}"
        self.assertRedirects(response, expected_url)

    def test_login_success(self):
        login = self.client.login(username='teacher', password='pass123')
        self.assertTrue(login)

    def test_student_list_view(self):
        self.client.login(username='teacher', password='pass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
        self.assertContains(response, "Math")

    def test_add_student_post(self):
        self.client.login(username='teacher', password='pass123')
        response = self.client.post(reverse('add_student'), {
            'name': 'Bob',
            'subject': 'Science',
            'marks': 88
        }, follow=True)
        self.assertEqual(Student.objects.count(), 2)
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'Science')

    def test_edit_student_post(self):
        self.client.login(username='teacher', password='pass123')
        response = self.client.post(reverse('edit_student', args=[self.student.id]), {
            'name': 'Alice Edited',
            'subject': 'Math',
            'marks': 99
        }, follow=True)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Alice Edited')
        self.assertEqual(self.student.marks, 99)
        self.assertContains(response, 'Alice Edited')

    def test_delete_student(self):
        self.client.login(username='teacher', password='pass123')
        response = self.client.get(reverse('delete_student', args=[self.student.id]), follow=True)
        self.assertEqual(Student.objects.count(), 0)
        self.assertNotContains(response, 'Alice')
