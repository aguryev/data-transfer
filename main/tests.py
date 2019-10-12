from django.test import TestCase
from django.utils import timezone
from .models import SecuredData

# Create your tests here.

class SecuredDataTests(TestCase):

	test_time = timezone.now()
	test_url = 'http://some.domain.com'
	test_file = 'http://path/to_file'

	def setUp(self):
		# file object
		f = SecuredData.create(
			description='Test File', 
			link=self.test_file, 
			is_file=True,
			)
		f.save()

		# URL object
		u = SecuredData.create(
			description='Test URL', 
			link=self.test_url, 
			is_file=False,
			)
		u.save()

	def test_url_secureddata_created(self):
		url = SecuredData.objects.get(description='Test URL')
		self.assertEqual(url.link, self.test_url)
		self.assertEqual(len(url.slug), 16)
		self.assertEqual(len(url.password), 10)
		#self.assertEqual(url.created, self.test_time)
		self.assertEqual(url.valid_until, url.created+timezone.timedelta(hours=24))
		self.assertEqual(url.visits, 0)
		self.assertFalse(url.is_file)

	def test_file_secureddata_created(self):
		file = SecuredData.objects.get(description='Test File')
		self.assertEqual(file.link, self.test_file)
		self.assertEqual(len(file.slug), 16)
		self.assertEqual(len(file.password), 10)
		#self.assertEqual(file.created, self.test_time)
		self.assertEqual(file.valid_until, file.created+timezone.timedelta(hours=24))
		self.assertEqual(file.visits, 0)
		self.assertTrue(file.is_file)
