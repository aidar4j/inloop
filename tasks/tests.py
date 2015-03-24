from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import UserProfile
from tasks.models import Task


class TaskModelTests(TestCase):
    def setUp(self):
        author = UserProfile.objects.create(
            username='unittest',
            first_name='unit',
            last_name='test',
            email='unittest@example.com',
            mat_num='12345678',
            is_staff=True,
            is_active=True,
            date_joined=timezone.now() - timezone.timedelta(days=1)

        )

        Task.objects.create(
            title='active_task',
            author=author,
            description='',
            publication_date=timezone.now() - timezone.timedelta(days=2),
            deadline_date=timezone.now() + timezone.timedelta(days=2),
            category='B',
            slug='active-task'
        )

        Task.objects.create(
            title='disabled_task',
            author=author,
            description='',
            publication_date=timezone.now() + timezone.timedelta(days=1),
            deadline_date=timezone.now() + timezone.timedelta(days=5),
            category='B',
            slug='disabled-task'
        )

    def test_task_is_active(self):
        active_task = Task.objects.get(title='active_task')
        disabled_task = Task.objects.get(title='disabled_task')

        self.assertTrue(active_task.is_active())
        self.assertFalse(disabled_task.is_active())

    def test_invalid_inputs(self):
        with self.assertRaises(ValidationError):
            Task.objects.create(publication_date='abc')

        with self.assertRaises(ValidationError):
            Task.objects.create(deadline_date='abc')
