from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest
import time

'''
Tests for the different use cases
'''
class UseCasesTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    '''
    Test case:
    - unregistered user opens the website
    - user clicks on "Sign Up"
    - user tries to register with a bad email address
    - user registers correctly
    '''
    def test_signup(self):

        #User opens homepage
        self.browser.get('http://marcopolver.pythonanywhere.com/')

        #The title has to be "Home"
        self.assertIn('Home', self.browser.title)

        #Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertIn('You are not logged in', paragraph)

        #The user opens the signup page
        signup_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Sign Up' in link.text][0]
        signup_link.click()

        #The new url has to be /signup/
        signup_url = self.browser.current_url
        self.assertEqual(signup_url, 'http://marcopolver.pythonanywhere.com/signup/')
        self.assertIn(self.browser.title, 'Sign Up')

        #The user fills the form
        username_box = self.browser.find_element_by_name('username')
        email_box = self.browser.find_element_by_name('email')
        password1_box = self.browser.find_element_by_name('password1')
        password2_box = self.browser.find_element_by_name('password2')
        name_box = self.browser.find_element_by_name('name')
        surname_box = self.browser.find_element_by_name('surname')
        major_box = Select(self.browser.find_element_by_name('major'))
        year_of_study = self.browser.find_element_by_name('year_of_study')
        submit_button = self.browser.find_element_by_name('submit')

        #The user writes his username and email address (wrong)
        username_box.send_keys('prova')
        email_box.send_keys('prova@gmail.com')
        password1_box.send_keys('giovannino95')
        password2_box.send_keys('giovannino95')
        name_box.send_keys('Prova')
        surname_box.send_keys('Uno')
        major_box.select_by_index(1)        #Ingegneria informatica triennale
        #year_of_study.send_keys('1')        #Primo anno
        submit_button.click()

        #The user must be in the same page since the registration was unsuccessful
        self.assertEqual(self.browser.current_url, signup_url)

        #An error message should appear
        error_message = [li.text for li in self.browser.find_elements_by_css_selector('li') if 'UniBG' in li.text][0]
        self.assertEqual(error_message, 'An email from UniBG is required')

        #The user refreshes the page
        self.browser.get(signup_url)

        #The user fills the form again
        username_box = self.browser.find_element_by_name('username')
        email_box = self.browser.find_element_by_name('email')
        password1_box = self.browser.find_element_by_name('password1')
        password2_box = self.browser.find_element_by_name('password2')
        name_box = self.browser.find_element_by_name('name')
        surname_box = self.browser.find_element_by_name('surname')
        major_box = Select(self.browser.find_element_by_name('major'))
        year_of_study = self.browser.find_element_by_name('year_of_study')
        submit_button = self.browser.find_element_by_name('submit')

        # The user writes his username and email address (wrong)
        username_box.send_keys('prova7')
        email_box.send_keys('prova@studenti.unibg.it')
        password1_box.send_keys('giovannino95')
        password2_box.send_keys('giovannino95')
        name_box.send_keys('Prova')
        surname_box.send_keys('Nove')
        major_box.select_by_index(1)  # Ingegneria informatica triennale
        # year_of_study.send_keys('1')        #Primo anno
        submit_button.click()

        time.sleep(1)

        #The user should see the login page
        #self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/login/')

    '''
    Test case:
    - user logs in
    - the homepage is opened
    - user opens his/her suggested-ads page
    '''
    def test_first_page(self):

        # User opens homepage
        self.browser.get('http://marcopolver.pythonanywhere.com/')

        # The title has to be "Home"
        self.assertIn('Home', self.browser.title)

        # Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertIn('You are not logged in', paragraph)

        # The user opens the signup page
        login_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Login' in link.text][0]
        login_link.click()

        # The new url has to be /login/
        login_url = self.browser.current_url
        self.assertEqual(login_url, 'http://marcopolver.pythonanywhere.com/login/')
        self.assertIn(self.browser.title, 'Login')

        #The user fills the form
        username_box = self.browser.find_element_by_name('username')
        password_box = self.browser.find_element_by_name('password')
        username_box.send_keys('ING_GES_M11')
        password_box.send_keys('bombastic24')

        #The user clicks the login button to log in
        submit_button = [button for button in self.browser.find_elements_by_css_selector('button') if 'Login' in button.text][0]
        submit_button.click()

        #The user should be in the homepage and see a greeting message
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/')

        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertEqual(paragraph, 'Hi ING_GES_M11!')

        #The user clicks on the personal page link
        personal_page_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'ING_GES_M11' in link.text][0]
        personal_page_link.click()

        #The user should be in their personal page
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/users/ING_GES_M11/profile')

        title = self.browser.find_element_by_css_selector('h2').text
        self.assertEqual(title, 'ING_GES_M11')

        self.browser.get('http://marcopolver.pythonanywhere.com/')

        #The user clicks on the "Suggested ads" link
        suggested_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Suggested' in link.text][0]
        suggested_link.click()

        time.sleep(5)  #Necessary for the algorhythm to be executed

        #The user should be in their personal suggested-ads page
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/users/ING_GES_M11/suggested')

        # The user should see a number of cards between 0 and 20 (included)
        cards = [card for card in self.browser.find_elements_by_class_name('card')]
        self.assertLessEqual(len(cards), 20)
        self.assertGreaterEqual(len(cards), 0)

        # The user logs out
        logout_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Logout' in link.text][0]
        logout_link.click()

        #time.sleep(10)

        # The user should be in the homepage
        time.sleep(2)

        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/')

        # Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertIn('You are not logged in', paragraph)

    def test_search_ad(self):
        # User opens homepage
        self.browser.get('http://marcopolver.pythonanywhere.com/')

        # The title has to be "Home"
        self.assertIn('Home', self.browser.title)

        # Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertIn('You are not logged in', paragraph)

        # The user opens the signup page
        login_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Login' in link.text][0]
        login_link.click()

        # The new url has to be /login/
        login_url = self.browser.current_url
        self.assertEqual(login_url, 'http://marcopolver.pythonanywhere.com/login/')
        self.assertIn(self.browser.title, 'Login')

        # The user fills the form
        username_box = self.browser.find_element_by_name('username')
        password_box = self.browser.find_element_by_name('password')
        username_box.send_keys('ING_GES_M11')
        password_box.send_keys('bombastic24')

        # The user clicks the login button to log in
        submit_button = [button for button in self.browser.find_elements_by_css_selector('button') if 'Login' in button.text][0]
        submit_button.click()

        # The user should be in the homepage and see a greeting message
        time.sleep(2)

        #self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/')

        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertEqual(paragraph, 'Hi ING_GES_M11!')

        # The user clicks on the "Search" link
        search_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Search' in link.text][0]
        search_link.click()

        # The user should be in the search page
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/search/')
        self.assertIn('Search', self.browser.title)

        # The user clicks on the "To book ads" link
        ads_link = [link for link in self.browser.find_elements_by_css_selector('a') if "To book ads" in link.text][0]
        ads_link.click()

        # The user should be in the search-ads page
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/search/ads/')
        self.assertIn('Search ad', self.browser.title)

        # The user sets the filters and searches the desired ads
        title_box = Select(self.browser.find_element_by_name('title_name'))
        quality_class_box = Select(self.browser.find_element_by_name('quality_class'))
        starting_price_box = self.browser.find_element_by_name('starting_price')
        ending_price_box = self.browser.find_element_by_name('ending_price')

        title_box.select_by_value('Titolo_0')
        quality_class_box.select_by_value('A')
        starting_price_box.send_keys('2')
        ending_price_box.send_keys('16')

        # The user clicks the submit button to start the search
        submit_button = self.browser.find_element_by_name('submit')
        submit_button.click()

        # The user should be redirected to the results page
        self.assertIn('http://marcopolver.pythonanywhere.com/search/ads/results', self.browser.current_url)
        self.assertIn('Search ad', self.browser.title)

        # The results should be coherent with the filters
        # Title coherence
        results_title = [title.text for title in self.browser.find_elements_by_class_name('card-title')]
        for title in results_title:
            self.assertEqual(title, 'Titolo_0')

        # Quality class coherence
        results_class = [str(paragraph.text).split('\n')[0][7:] for paragraph in self.browser.find_elements_by_class_name('card-text')]
        for q_class in results_class:
            self.assertEqual(q_class, 'A')

        # Price coherence
        results_price = [str(paragraph.text).split('\n')[1][7:] for paragraph in
                         self.browser.find_elements_by_class_name('card-text')]
        for price in results_price:
            self.assertGreaterEqual(float(price), 2)
            self.assertLessEqual(float(price), 16)

        # The user logs out
        logout_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Logout' in link.text][0]
        logout_link.click()

        # time.sleep(10)

        # The user should be in the homepage
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/')

        # Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertIn('You are not logged in', paragraph)



    def test_search_user(self):
        # User opens homepage
        self.browser.get('http://marcopolver.pythonanywhere.com/')

        # The title has to be "Home"
        self.assertIn('Home', self.browser.title)

        # Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertIn('You are not logged in', paragraph)

        # The user opens the login page
        login_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Login' in link.text][0]
        login_link.click()

        # The new url has to be /login/
        login_url = self.browser.current_url
        self.assertEqual(login_url, 'http://marcopolver.pythonanywhere.com/login/')
        self.assertIn(self.browser.title, 'Login')

        # The user fills the form
        username_box = self.browser.find_element_by_name('username')
        password_box = self.browser.find_element_by_name('password')
        username_box.send_keys('ING_GES_M11')
        password_box.send_keys('bombastic24')

        # The user clicks the login button to log in
        submit_button = [button for button in self.browser.find_elements_by_css_selector('button') if 'Login' in button.text][0]
        submit_button.click()

        # The user should be in the homepage and see a greeting message
        time.sleep(2)
        #self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/')
        

        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertEqual(paragraph, 'Hi ING_GES_M11!')

        # The user clicks on the "Search" link
        search_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Search' in link.text][0]
        search_link.click()

        # The user should be in the search page
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/search/')
        self.assertIn('Search', self.browser.title)

        # The user clicks on the "To users" link
        users_link = [link for link in self.browser.find_elements_by_css_selector('a') if "To users" in link.text][0]
        users_link.click()

        # The user should be in the search-users page
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/search/users/')
        self.assertIn('Search student', self.browser.title)

        # The user sets the filters and searches the desired ads
        major_box = Select(self.browser.find_element_by_name('major'))
        year_of_study_box = Select(self.browser.find_element_by_name('year_of_study'))
        username_box = self.browser.find_element_by_name('username')

        major_box.select_by_value('ING_INF_M')
        year_of_study_box.select_by_value('2')
        username_box.send_keys('ING_INF_M')

        # The user clicks the submit button to start the search
        submit_button = self.browser.find_element_by_name('submit')
        submit_button.click()

        # The user should be redirected to the results page
        self.assertIn('http://marcopolver.pythonanywhere.com/search/users/results', self.browser.current_url)
        self.assertIn('Search student', self.browser.title)

        # The results should be coherent with the filters
        # Username coherence
        results_users = [user.text for user in self.browser.find_elements_by_id('student-username')]
        for user in results_users:
            self.assertIn('ING_INF_M', user)

        # Major coherence
        results_major = [major.text[7:] for major in self.browser.find_elements_by_id('student-major')]
        for major in results_major:
            self.assertEqual(major, 'ING_INF_M')

        # Year of study coherence
        results_yos = [yos.text[15:] for yos in self.browser.find_elements_by_class_name('student-yos')]
        for yos in results_yos:
            self.assertEqual(yos, '2')

        # The user logs out
        logout_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Logout' in link.text][0]
        logout_link.click()

        # time.sleep(10)

        # The user should be in the homepage
        self.assertEqual(self.browser.current_url, 'http://marcopolver.pythonanywhere.com/')

        # Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('h1').text
        self.assertIn('You are not logged in', paragraph)





if(__name__ == '__main__'):
    unittest.main()