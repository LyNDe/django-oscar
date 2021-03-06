from django_dynamic_fixture import G
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail

from oscar.test import WebTestCase
from oscar.apps.customer.models import CommunicationEventType


class TestAnAdmin(WebTestCase):

    def setUp(self):
        self.staff = G(User, is_staff=True, username='1234')
        self.commtype = CommunicationEventType.objects.create(
            code='PASSWORD_RESET', name="Password reset",
            category=CommunicationEventType.USER_RELATED)

    def test_can_preview_an_email(self):
        list_page = self.app.get(reverse('dashboard:comms-list'),
                                 user=self.staff)
        update_page = list_page.click('Edit')
        form = update_page.form
        form['email_subject_template'] = 'Hello {{ user.username }}'
        form['email_body_template'] = 'Hello {{ user.username }}'
        form['email_body_html_template'] = 'Hello {{ user.username }}'
        preview = form.submit('show_preview')
        self.assertTrue('Hello 1234' in preview.content)

    def test_can_send_a_preview_email(self):
        list_page = self.app.get(reverse('dashboard:comms-list'),
                                 user=self.staff)
        update_page = list_page.click('Edit')
        form = update_page.form
        form['email_subject_template'] = 'Hello {{ user.username }}'
        form['email_body_template'] = 'Hello {{ user.username }}'
        form['email_body_html_template'] = 'Hello {{ user.username }}'
        form['preview_email'] = 'testing@example.com'
        form.submit('send_preview')

        self.assertEqual(len(mail.outbox), 1)