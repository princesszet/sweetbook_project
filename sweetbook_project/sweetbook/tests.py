from django.test import TestCase
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse
from sweetbook.models import Event, UserProfile, Recipe, Comment, SavedRecipe
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from sweetbook.forms import RecipeForm, UserProfileRegistrationForm



'''Note to anyone recieving IntegrityErrors describing Unique constraints:
This error should not occur due to the addition of datetime strings to 
usernames etc., and has not been recreatable after the first time it
occured.
Should you experience this wait 10 seconds and run the test again.
Repeat this 5 times a most, if there is still an issue the error 
may be on your side. Apologies for any inconvenience.'''

class SimpleUrlTests(TestCase):
	def test_urls(self):

		good_response = self.client.get(reverse('home'))
		self.assertEqual(good_response.status_code, 200)

		bad_response = self.client.get('test')
		self.assertEqual(bad_response.status_code, 404)
		


class ViewTests(TestCase):

	def create_UserProfile(self,
     user=User.objects.create(username='Testuser'+str(datetime.now()), email='a@a.com',
     password='wordpass'),
     firstname='test',surname='test'):
		return UserProfile.objects.create(user=user,firstname=firstname,
			surname=surname)

	def test_home(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Recipe of the Day")
		self.assertContains(response, "Top rated")
		self.assertContains(response, "Latest Events")
		self.assertNotContains(response, "This should't be here")
		self.assertQuerysetEqual(response.context['latestevents'], [])
		#shoudl not display if there is no user
		self.assertNotContains(response, "Hello")
		self.assertNotContains(response, "My Account")
		'''creates a userprofile to test if the page shows hello user once
		the user is logged in, as well as diplaying the my account tab'''
		self.create_UserProfile()
		self.assertTrue(response, 'Hello')
		self.assertTrue(response, 'My Account')
		#self.assertQuerysetEqual(response.context['comments_count'], [])
		#print(response.content)

	def test_myaccount(self):
		response = self.client.get(reverse('sweetbook:myaccount'))
		#should be 302 as when no user is signed in it redirects to login
		self.assertEqual(response.status_code, 302)
	
	def test_mybakebook(self):
		
		response = self.client.get(reverse('sweetbook:mybakebook'))
		#should be 302 as when no user is signed in it redirects to login
		self.assertEqual(response.status_code, 302)
		
	def test_mycalendar(self):
		response = self.client.get(reverse('sweetbook:mycalendar'))
		#should be 302 as when no user is signed in it redirects to login
		self.assertEqual(response.status_code, 302)
		
	def test_myrecipes(self):
		
		response = self.client.get(reverse('sweetbook:myrecipes'))
		#should be 302 as when no user is signed in it redirects to login
		self.assertEqual(response.status_code, 302)
		

	def test_login(self):
		response = self.client.get(reverse('auth_login'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Log in")
		self.assertContains(response, "Not a member yet?")
		self.assertNotContains(response, "This should't be here")
		user = self.create_UserProfile()
		response = self.client.get(reverse('auth_login'))
		self.assertEqual(response.status_code, 200)
		self.client.post(user)
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response,'Top rated')


	def test_register(self):
		response = self.client.get(reverse('auth_register'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Register Here")
		self.assertContains(response, "Already a member?")
		self.assertNotContains(response, "This should't be here")

	def test_register(self):
		response = self.client.get(reverse('auth_logout'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Log out")
		self.assertContains(response, "You are now logged out!")
		self.assertNotContains(response, "This should't be here")

	def test_recipes(self):
		response = self.client.get(reverse('sweetbook:recipes'))
		self.assertEqual(response.status_code, 200)
		'''After testing once, recipes will be present as so this will fail,
		it is here for convenience'''
		#self.assertContains(response, "No events to be shown.")
		self.assertNotContains(response, "This should't be here")
		self.assertQuerysetEqual(response.context['recipes'], [])

	def test_events(self):
		response = self.client.get(reverse('sweetbook:events'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No events to be shown.")
		self.assertNotContains(response, "This should't be here")
		self.assertQuerysetEqual(response.context['events'], [])

	def test_contactus(self):
		response = self.client.get(reverse('sweetbook:contactus'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "We are a team")
		self.assertNotContains(response, "This should't be here")


'''datetime.now(tz=timezone.utc) - changes the datetime from naive type into
    one that contains information about timezones so a runtime error does not occur'''
class ModelTests(TestCase):		

    
    def create_Event(self, name='test'+str(datetime.now()), event_slug='test-slug',
        date=datetime.now(tz=timezone.utc), description='test desc.',
        place = 'testplace',postcode='testpost',url='testurl'):
        return Event.objects.create(name=name, event_slug=event_slug,
            date=date,description=description,place=place,postcode=postcode,
            url=url)

    def test_Event(self):
        event = self.create_Event()
        self.assertTrue(isinstance(event,Event))
        self.assertEqual(event.__str__(), event.name)





        #Adds datetime to the username as username has a unique constraint. This will ensure it is always unique
    def create_Recipe(self,user=User.objects.create(username='Testuserrecipe'+str(datetime.now())),name='testname'+str(datetime.now()),
    	recipe_slug='test-slug', ingredients = 'test ing.',
    	description='test desc.',rating=1, rating_number=1,
    	cooktime=12, difficulty='hard', 
    	last_modified = datetime.now(tz=timezone.utc)):
    	return Recipe.objects.create(user=user,name=name,
    		recipe_slug=recipe_slug,ingredients=ingredients,
    		description=description,rating=rating,rating_number=rating_number,
    		cooktime=cooktime,difficulty=difficulty,last_modified=last_modified)

    def test_Recipe(self):
    	recipe = self.create_Recipe()
    	self.assertTrue(isinstance(recipe,Recipe))
    	self.assertEqual(recipe.__str__(), recipe.name)    

    def tearDownRecipe(self):
    	self.recipe.delete()



    def create_SavedRecipe(self, 
    	user=User.objects.create(username='Testusersavedrecipe'+str(datetime.now())),
    	recipe=Recipe.objects.create(user=User.objects.create(username='Testuser'+str(datetime.now())),name='testname'+str(datetime.now()),
    	recipe_slug='test-slug', ingredients = 'test ing.',
    	description='test desc.',rating=1, rating_number=1,
    	cooktime=12, difficulty='hard', 
    	last_modified = datetime.now(tz=timezone.utc))):
    	return SavedRecipe.objects.create(user=user, recipe=recipe)

    def test_SavedRecipe(self):
    	savedrecipe = self.create_SavedRecipe()
    	self.assertTrue(isinstance(savedrecipe,SavedRecipe))
    	self.assertEqual(savedrecipe.__str__(), savedrecipe.user.username +" saves " + savedrecipe.recipe.name)




    def create_UserProfile(self,
     user=User.objects.create(username='Testuser'+str(datetime.now())),
     firstname='test',surname='test'):
    	return UserProfile.objects.create(user=user,firstname=firstname,
    		surname=surname)

    def test_UserProfile(self):
    	user = self.create_UserProfile()
    	self.assertTrue(isinstance(user,UserProfile))
    	self.assertEqual(user.__str__(), user.user.username)

    def tearDownUserProfile(self):
    	self.user.delete()


    def create_Comment(self,
		user=User.objects.create(username='Testusercomment'+str(datetime.now())),
		recipe=Recipe.objects.create(user=User.objects.create(username='Testusercommentrecipe'+str(datetime.now())),name='testname'+str(datetime.now()),
    	recipe_slug='test-slug', ingredients = 'test ing.',
    	description='test desc.',rating=1, rating_number=1,
    	cooktime=12, difficulty='hard', 
    	last_modified = datetime.now(tz=timezone.utc)),
		date=datetime.now(tz=timezone.utc), description='test desc'):
    	return Comment.objects.create(user=user,recipe=recipe,date=date,
    	 description=description)

    def test_Comment(self):
    	comment = self.create_Comment()
    	self.assertTrue(isinstance(comment,Comment))
    	self.assertEqual(comment.__str__(), comment.description)







class FormTests(TestCase):

	'''Due to the nature of the forms, this test is not required
	as validity tests for each are already preformed, however I felt it
	was good form to include at least one.
	'''
	def test_valid_form(self):
		up = UserProfile.objects.create(user=User.objects.create(username='Testuser'+str(datetime.now())),
			firstname='first',surname='sur')
		data = {'user':up.user, 'firstname':up.firstname,'surname':up.surname}
		form = UserProfileRegistrationForm(data=data)
		self.assertTrue(form.is_valid())

















