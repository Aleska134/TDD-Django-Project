from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from posts.forms import PostCreationForm
from django.http.request import HttpRequest
from model_bakery import baker
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class PostCreationTest(TestCase):
    def setUp(self):
        self.url = reverse('create_post')
        self.template_name = 'posts/createpost.html'
        self.form_class = PostCreationForm
        self.title = 'Sample title'
        self.body = 'Sample body for the sample test'
        
        User.objects.create_user(
            username = 'testuser',
            email='testuser@app.com',
            password='testpassword123##'
        )
        
    def test_post_creation_page_exists(self):
        self.client.login(username = 'testuser',password='testpassword123##')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response,self.template_name)
        
        form = response.context.get('form',None)
        
        self.assertIsInstance(form,self.form_class)
        
        
    def test_post_creation_form_creates_posts(self):
        post_request = HttpRequest()
        
        
        post_request.user = baker.make(User)
        
        post_data = {
            'title':self.title,
            'body':self.body
        }
        post_request.POST = post_data
        
        form = self.form_class(post_request.POST)
        
        self.assertTrue(form.is_valid())
        
        post_obj = form.save(commit=False)
        self.assertIsInstance(post_obj,Post)
        
        post_obj.author = post_request.user
        
        post_obj.save()
        
        self.assertEqual(Post.objects.count(),1)
        
    def test_post_creation_requires_login(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code,HTTPStatus.FOUND)
        self.assertRedirects(response,expected_url='/accounts/login/?next=/create_post/')