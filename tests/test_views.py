from django.contrib.auth import SESSION_KEY
from django.core.urlresolvers import reverse
from django.test import TestCase

from tests.accounts.mixins import SimpleAccountsData
from tests.decorators import assert_login


class ProtectedLogoutTest(SimpleAccountsData, TestCase):
    def test_method_not_allowed(self):
        for url in [reverse("logout"), reverse("admin:logout")]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 405)

    @assert_login("bob", "secret")
    def test_logout(self):
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn(SESSION_KEY, self.client.session)
