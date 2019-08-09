from django.test import TestCase
from sales import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.
'''
Test home view
'''
class HomeViewTest(TestCase):

    #Test the template used for the view
    def test_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

'''
Test first page (suggested ads)
'''
class ViewsTest(TestCase):

    ad_id = 0

    def setUp(self):

        test_user = models.User.objects.create(username='test_user', password='giovannino95')
        test_user.save()
        test_student = models.StudentProfile.objects.create(user=test_user, name='Test', surname='Student', major='ING_GES_M', year_of_study=2)
        test_student.save()
        title = models.Title.objects.create(name='Test title', isbn='800', description='test',
                                            description_author=test_user, category='STA')
        title.save()
        ad = models.BookAd.objects.create(title=title, seller=test_user, description="Test ad", price=10, quality_class='A', photo='ads/book.jpg')
        ad.save()
        self.ad_id = ad.pk

    '''
    Test this case:
    - user logs in
    - user opens suggested ads
    - user logs out
    - user logs in
    - user opens suggested ads
    '''
    def test_first_page_success_case(self):
        #Initial number of clustering runs has to be 0
        first_count = models.ClusteringInfo.objects.count()
        self.assertEqual(first_count, 0)

        #The user has to log in
        response = self.client.post('/login/', {'username': 'test_user', 'password': 'giovannino95'})
        self.assertEqual(response.status_code, 200)

        #The user opens the suggested-ads page
        response = self.client.get('/users/test_user/suggested')
        self.assertEqual(response.status_code, 200)

        #The current number of clustering runs has to be increased
        current_count = models.ClusteringInfo.objects.count()
        self.assertEqual(current_count, first_count+1)

        #Student's logout
        response = self.client.get('/logout/')

        #The user has to log in
        response = self.client.post('/login/', {'username': 'test_user', 'password': 'giovannino95'})
        self.assertEqual(response.status_code, 200)

        #The user opens the suggested-ads page
        response = self.client.get('/users/test_user/suggested')
        self.assertEqual(response.status_code, 200)

        #The current number of clustering runs has to be the same as before
        current_count = models.ClusteringInfo.objects.count()
        self.assertEqual(current_count, first_count + 1)

    #Test case in which we try to get the suggested ads of a user that doesn't exist
    def test_first_page_404(self):

        #The user has to log in
        response = self.client.post('/login/', {'username': 'test_user', 'password': 'giovannino95'})
        self.assertEquals(response.status_code, 200)

        # The user opens the suggested-ads page
        response = self.client.get('/users/unknown/suggested')
        self.assertEquals(response.status_code, 404)

    #Test case in which we try to get the details of an ad that doesn't exist
    def test_ad_details_404(self):

        # The user has to log in
        response = self.client.post('/login/', {'username': 'test_user', 'password': 'giovannino95'})
        self.assertEquals(response.status_code, 200)

        # The user opens the suggested-ads page
        response = self.client.get('/ads/000')
        self.assertEquals(response.status_code, 404)

    #Test the template used while showing the details about an ad
    def test_ad_details_template(self):

        response = self.client.get('/ads/'+str(self.ad_id))
        self.assertTemplateUsed(response, 'ads.html')

    #Test case in which we try to get the details about a student that doesn't exist
    def test_profile_404(self):

        response = self.client.get('/users/unknown/profile')
        self.assertEqual(response.status_code, 404)

    # Test the template used while showing the details about a student
    def test_profile_template(self):
        response = self.client.get('/users/test_user/profile')
        self.assertTemplateUsed(response, 'student_profile.html')

    # Test the template used while showing the search page
    def test_search_template(self):
        response = self.client.get('/search/')
        self.assertTemplateUsed(response, 'search.html')

    # Test the template used while showing the search ads page
    def test_search_ads_template(self):
        response = self.client.get('/search/ads/')
        self.assertTemplateUsed(response, 'search_ad.html')

    # Test the template used while showing the search users page
    def test_search_students_template(self):
        response = self.client.get('/search/users/')
        self.assertTemplateUsed(response, 'search_student.html')


