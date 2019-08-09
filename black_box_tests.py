from selenium import webdriver
from selenium.webdriver.support.ui import Select
import unittest
import time

'''
Test case:
- unregistered user opens the website
- user clicks on "Sign Up"
- user tries to register with a bad email address
- user registers correctly
'''
class SignUpTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    #Test titolo homepage
    def test_signup(self):

        #User opens homepage
        self.browser.get('http://localhost:8000/')

        #The title has to be "Home"
        self.assertIn('Home', self.browser.title)

        #Since the user hasn't logged in, a paragraph should say "You are not logged in"
        paragraph = self.browser.find_element_by_css_selector('p').text
        self.assertIn('You are not logged in', paragraph)

        #The user opens the signup page
        signup_link = [link for link in self.browser.find_elements_by_css_selector('a') if 'Sign Up' in link.text][0]
        signup_link.click()

        #The new url has to be /signup/
        signup_url = self.browser.current_url
        self.assertEqual(signup_url, 'http://localhost:8000/signup/')

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
        username_box.send_keys('prova')
        email_box.send_keys('prova@studenti.unibg.it')
        password1_box.send_keys('giovannino95')
        password2_box.send_keys('giovannino95')
        name_box.send_keys('Prova')
        surname_box.send_keys('Uno')
        major_box.select_by_index(1)  # Ingegneria informatica triennale
        # year_of_study.send_keys('1')        #Primo anno
        submit_button.click()

        time.sleep(1)

        #The user should see the login page
        self.assertEqual(self.browser.current_url, 'http://localhost:8000/login/')

if(__name__ == '__main__'):
    unittest.main()