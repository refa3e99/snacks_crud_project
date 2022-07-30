from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack


# Create your tests here.
class SnackTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@test.com',
            password='test@12345'
        )
        self.snack = Snack.objects.create(
            title='Test',
            purchaser=self.user,
            description='Snacks'
        )

    def test_list_status(self):
        url = reverse('snacks_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_str_method(self):
        self.assertEqual(str(self.snack), 'Test')

    def test_content(self):
        self.assertEqual(f"{self.snack.title}", "Test")
        self.assertEqual(f"{self.snack.purchaser}", self.user.__str__())
        self.assertEqual(f"{self.snack.description}", "Snacks")

# test views
    def test_list_view(self):
        url = reverse('snacks_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snacks_list.html')

    def test_detail_view(self):
        url = reverse('snacks_detail', args=[self.snack.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snacks_detail.html')

    def test_create_view(self):
        url = reverse('snacks_create')
        data = {
            'title': 'Test create',
            'purchaser': self.user.id,
            'description': 'test',
        }
        response = self.client.post(path=url, data=data, follow=True)
        self.assertRedirects(response, reverse('snacks_detail', args=[2]))
        self.assertTemplateUsed(response, 'snacks_detail.html')
        self.assertContains(response, 'test')

    def test_update_view(self):
        data = {
            'title': 'Test update',
            'purchaser': self.user.id,
            'description': 'update',
        }
        response = self.client.post(
            reverse("snacks_update", args="1"), data
        )
        self.assertRedirects(response, reverse("snacks_detail", args="1"))

    def test_delete_view(self):
        response = self.client.get(reverse('snacks_delete', args='1'))
        self.assertEqual(response.status_code, 200)

    # templates tests
    def test_list_template(self):
        url = reverse('snacks_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snacks_list.html')

    def test_create_template(self):
        url = reverse('snacks_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snacks_create.html')

    def test_update_template(self):
        url = reverse('snacks_update', args=[1])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snacks_update.html')

    def test_delete_template(self):
        url = reverse('snacks_delete', args=[1])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snacks_delete.html')

    def test_detail_template(self):
        url = reverse('snacks_detail', args=[1])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snacks_detail.html')
