import os
import shutil
from tempfile import mkdtemp

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings, tag
from django.urls import reverse

from inloop.accounts.forms import User
from inloop.solutions.models import Solution, SolutionFile
from inloop.tasks.models import Category, Task
from inloop.testrunner.models import TestOutput, TestResult

from tests.integration.tools import MessageTestCase
from tests.solutions.mixins import SolutionsData

FIBONACCI = """
public class Fibonacci {
    public static int fib(final int x) {
    if (x < 0) {
        throw new IllegalArgumentException("x must be greater than or equal zero");
    }

    int a = 0;
    int b = 1;

    for (int i = 0; i < x; i++) {
        int sum = a + b;
        a = b;
        b = sum;
    }

    return a;
    }

    /*
     * This string is just here for testing purposes.
     */
}
"""

TEST_MEDIA_ROOT = mkdtemp()


@tag("slow")
@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class SolutionUploadTest(SolutionsData, MessageTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.assertTrue(self.client.login(username="bob", password="secret"))
        self.url = reverse("solutions:upload", kwargs={"slug": self.task.slug})

    def test_solution_upload_without_files(self):
        """Validate that if no files were uploaded, a meaningful message is emitted."""
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertResponseContainsMessage(
            "You haven't uploaded any files.",
            self.Levels.ERROR,
            response
        )

    def test_solution_upload_with_multiple_files(self):
        """Test the solution upload."""
        file_1 = SimpleUploadedFile("Fibonacci1.java", "class Fibonacci1 {}".encode())
        file_2 = SimpleUploadedFile("Fibonacci2.java", "class Fibonacci2 {}".encode())
        response = self.client.post(self.url, data={
            "uploads": [file_1, file_2]
        }, follow=True)
        self.assertResponseContainsMessage(
            "Your solution has been submitted to the checker.",
            self.Levels.SUCCESS,
            response
        )
        # Extract all files in media root
        file_names = [
            item for sublist in list(l for _, _, l in os.walk(TEST_MEDIA_ROOT))
            for item in sublist
        ]
        self.assertIn("Fibonacci1.java", file_names)
        self.assertIn("Fibonacci2.java", file_names)

    def test_invalid_solutions_fail(self):
        """Validate that invalid solutions fail."""

    def test_valid_solutions_succeed(self):
        """Validate that valid solutions succeed."""

    def test_zip_download(self):
        """Test wether zips can be downloaded."""

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_MEDIA_ROOT)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class SolutionDetailViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not os.path.isdir(TEST_MEDIA_ROOT):
            os.makedirs(TEST_MEDIA_ROOT)

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(id=1337, name="Category 1")
        cls.task = Task.objects.create(
            pubdate="2000-01-01 00:00Z",
            category=cls.category,
            title="Fibonacci",
            slug="task"
        )
        cls.bob = User.objects.create_user(
            username="bob",
            email="bob@example.org",
            password="secret"
        )
        cls.solution = Solution.objects.create(author=cls.bob, task=cls.task, passed=True)
        cls.solution_file = SolutionFile.objects.create(
            solution=cls.solution,
            file=SimpleUploadedFile('Fibonacci.java', FIBONACCI.encode())
        )
        cls.test_result = TestResult.objects.create(
            solution=cls.solution,
            stdout="This is the STDOUT output.",
            stderr="This is the STDERR output.",
            return_code=0,
            time_taken=1.0
        )
        cls.test_output = TestOutput.objects.create(result=cls.test_result, name="", output="")

    def setUp(self):
        self.assertTrue(self.client.login(username="bob", password="secret"))
        self.url = reverse("solutions:detail", kwargs={
            "slug": self.task.slug, "scoped_id": self.solution.scoped_id
        })
        super().setUp()

    def test_displayed_media(self):
        """Validate that static and dynamic media is displayed correctly."""

        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Congratulations, your solution passed all tests.")
        self.assertContains(response, "Fibonacci.java")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_MEDIA_ROOT)
        super().tearDownClass()
