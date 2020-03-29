import os
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from treebay.models import UserProfile
from treebay.models import User
from treebay.models import Category
from treebay.models import Plant


class ProjectStructureTests(TestCase):
    """
    Simple tests to probe the file structure.
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.treebay_app_dir = os.path.join(self.project_base_dir, 'treebay')
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.treebay_templates_dir = os.path.join(self.templates_dir, 'treebay')
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')

    def test_treebay_app_created(self):
        """
        Determines whether the Treebay app has been created.
        """
        directory_exists = os.path.isdir(self.treebay_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.treebay_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.treebay_app_dir, 'views.py'))

        self.assertTrue(directory_exists, "The treebay app directory does not exist.")
        self.assertTrue(is_python_package, "The treebay directory is missing init file.")
        self.assertTrue(views_module_exists, "The treebay directory is missing views.")

    def test_is_treebay_app_configured(self):
        """
        Is there an INSTALLED_APPS list?
        """
        is_app_configured = 'treebay' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configured, "The treebay app is missing from setting's INSTALLED_APPS list.")

    def test_templates_directory_exists(self):
        """
        Does the templates/ directory exist?
        """
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, "Project's templates directory does not exist.")

    def test_treebay_templates_directory_exists(self):
        """
        Does the templates/treebay/ directory exist?
        """
        directory_exists = os.path.isdir(self.treebay_templates_dir)
        self.assertTrue(directory_exists, "The Treebay templates directory does not exist.")

    def test_does_static_directory_exist(self):
        """
        Tests whether the static directory exists in the correct location.
        """
        does_static_dir_exist = os.path.isdir(self.static_dir)
        does_images_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images'))
        does_profile_pictures_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images/profile_pictures'))
        does_plants_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images/plants'))

        self.assertTrue(does_static_dir_exist, "The static directory was not found in the expected location.")
        self.assertTrue(does_images_static_dir_exist, "The images subdirectory was not found in static directory.")
        self.assertTrue(does_profile_pictures_static_dir_exist, "The profile_pictures subdirectory was not found in "
                                                                "static/images directory.")

    def test_static_configuration(self):
        """
        Performs a number of tests on Django project's settings in relation to static files.
        """
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists, "The settings.py module does not have the variable STATIC_DIR defined.")

        expected_path = os.path.normpath(self.static_dir)
        static_path = os.path.normpath(settings.STATIC_DIR)
        self.assertEqual(expected_path, static_path, "The value of STATIC_DIR does not equal the expected path.")

        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, "The STATICFILES_DIRS is not present in project's settings.py module.")

        staticfiles_dirs_exists = 'STATIC_URL' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, "The STATIC_URL variable has not been defined in settings.py.")


class DatabaseConfigurationTests(TestCase):
    """
    Test whether the database is configured in correct way,
    """

    def does_gitignore_include_database(self, path):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        f = open(path, 'r')

        for line in f:
            line = line.strip()

            if line.startswith('db.sqlite3'):
                return True

        f.close()
        return False

    def test_databases_variable_exists(self):
        """
        Does the DATABASES settings variable exist?
        """
        self.assertTrue(settings.DATABASES, "Settings module does not have a DATABASES variable.")



class CategoryTests(TestCase):

    def setUp(self):
        category_py = Category.objects.get_or_create(name='Aloe Vera')
        Category.objects.get_or_create(name='Orchid')

    def test_slug_line_creation(self):
        """
        Check that when a category is created, an appropriate slug is created
        """
        category = Category.objects.get(name="Aloe Vera")
        self.assertEquals(category.slug, "aloe-vera")


# class IndexViewTests(TestCase):
#     def test_index_with_no_categories(self):
#         """
#         If no categories exists, the appropriate message should be displayed.
#         """
#
#         response = self.client.get(reverse('treebay:dashboard'))
#
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'There are no categories present.')
#         self.assertQuerysetEqual(response.context['categories'], [])


class PlantTests(TestCase):
    def test_slug_line_creation(self):
        """
        Check that when a plant is created, an appropriate slug is created
        """
        user = User(username="test")
        user.save()
        user_profile = UserProfile(user_id=user.id)
        user_profile.save()
        plant = Plant(owner=user_profile, name="Very beautiful plant")
        plant.save()

        self.assertEquals(plant.slug, "very-beautiful-plant")


class AdminInterfaceTests(TestCase):
    """
    Tests that examines the authentication functionality, and admin interface changes.
    """

    def setUp(self):
        """
        Create a superuser account for use in testing.
        """
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')

    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200, "The admin interface is not accessible.")

    def test_models_present(self):
        """
        Checks whether the two models are present within the admin interface homepage
        """
        response = self.client.get('/admin/')
        response_body = response.content.decode()

        # Check each model is present.
        self.assertTrue('Categories' in response_body, "The Category model was not found in the admin interface.")
        self.assertTrue('Plants' in response_body, "The Plant model was not found in the admin interface.")


class PopulationScriptTests(TestCase):
    """
    Tests whether the population script puts the expected data into a test database.
    """

    def setUp(self):
        """
        Imports and runs the population script, calling the populate() method.
        """
        try:
            import populate_treebay
        except ImportError:
            raise ImportError("Populate Treebay could not be imported. Check it's in the right location.")

        if 'populate' not in dir(populate_treebay):
            raise NameError("The populate() function does not exist in the populate_treebay module.")

        # Call the population script -- any exceptions raised here do not have fancy error messages to help readers.
        populate_treebay.populate()

    def test_categories(self):
        """
        Test if there are categories from populate_treebay -- eg houseplants, allergy friendly and outdoor .
        """
        categories = Category.objects.filter()
        categories_len = len(categories)
        categories_strs = map(str, categories)

        self.assertTrue(categories_len > 0, "Expecting more than 0 categories after running populating script.")
        self.assertTrue('houseplants' in categories_strs, "Category 'houseplants' was expected but it was not created")

    def test_plants(self):
        """
        Test if there are plants from populate_treebay -- eg Spiky boi
        """
        plants = Plant.objects.filter()
        plants_len = len(plants)
        plants_strs = map(str, plants)

        self.assertTrue(plants_len > 0, "Expecting more than 0 plants after running populating script.")
        self.assertTrue('Spiky boi' in plants_strs, "Plant 'Spiky boi' was expected but it was not created")

    def test_users(self):
        """
        Test if there are users from populate_treebay -- eg alice
        """
        users = User.objects.filter()
        users_len = len(users)
        users_strs = map(str, users)

        self.assertTrue(users_len > 0, "Expecting more than 0 users after running populating script.")
        self.assertTrue('alice' in users_strs, "User 'alice' was expected but it was not created")