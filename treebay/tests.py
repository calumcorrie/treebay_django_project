import os
from django.test import TestCase
from django.urls import reverse, resolve
from django.conf import settings
from treebay.models import UserProfile
from treebay.models import User
from treebay.models import Category
from treebay.models import Plant
from django.core.files import File


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
        does_img_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'img'))
        does_profile_pictures_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'img/profile_pictures'))
        does_plants_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'img/plants'))
        does_www_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'img/www'))
        does_svg_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'img/svg'))

        self.assertTrue(does_static_dir_exist, "The static directory was not found in the expected location.")
        self.assertTrue(does_img_static_dir_exist, "The images subdirectory was not found in static directory.")
        self.assertTrue(does_profile_pictures_static_dir_exist, "The profile_pictures subdirectory was not found in "
                                                                "static/img directory.")
        self.assertTrue(does_plants_static_dir_exist, "The plants subdirectory was not found in static/img directory.")
        self.assertTrue(does_www_static_dir_exist, "The www subdirectory was not found in static/img directory.")
        self.assertTrue(does_svg_static_dir_exist, "The svg subdirectory was not found in static/img directory.")

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

    def test_does_gitignore_include_database(self):
        """
        Takes the path to a .gitignore file, and checks to see whether the db.sqlite3 database is present in that file.
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()
        gitignore_path = os.path.join(git_base_dir, '.gitignore')
        f = open(gitignore_path, 'r')

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


class PlantTests(TestCase):
    def test_slug_line_creation(self):
        """
        Check that when a plant is created, an appropriate slug is created
        """
        user = User.objects.get_or_create(username="alice")[0]
        user_profile = UserProfile.objects.get_or_create(user_id=user.id)[0]
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

    @classmethod
    def setUpClass(cls):
        """
        Imports and runs the population script, calling the populate() method.
        """
        super().setUpClass()
        try:
            import population_script
        except ImportError:
            raise ImportError("Populate Treebay could not be imported. Check it's in the right location.")

        if 'populate' not in dir(population_script):
            raise NameError("The populate() function does not exist in the populate_treebay module.")

        # Call the population script -- any exceptions raised here do not have fancy error messages to help readers.
        population_script.populate()

    @classmethod
    def tearDownClass(cls):
        plants = Plant.objects.filter()
        for plant in plants:
            plant.picture.delete()
        users = UserProfile.objects.filter()
        for user in users:
            user.picture.delete()
        super().tearDownClass()

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


class FormTests(TestCase):
    """
    Checks URL mappings and server output.
    """

    def test_about_link_in_index_page(self):
        """
        Checks if there is a link to about page at the index page.
        """
        response = self.client.get(reverse('treebay:index'))
        content = response.content.decode()

        self.assertTrue('<a href="/treebay/about/">About</a>' in content)


class ViewExistsTests(TestCase):
    """
    Validate the behaviour by views.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # create a user (alice) and a plant
        user = User.objects.get_or_create(username="alice")[0]
        cls.user_id = user.id
        user_profile = UserProfile.objects.get_or_create(user_id=cls.user_id)[0]
        user_profile.picture.save(user_profile.user.username + str(user_profile.id) + ".jpg",
                                  File(open('./static/img/profile_pictures/alice.jpg', 'rb')))
        user_profile.save()

        cls.plant = Plant(owner=user_profile, name="Test Plant", slug='test-plant')
        cls.plant.save()
        cls.plant.picture.save(cls.plant.slug + str(cls.plant.id) + ".jpg",
                               File(open('./static/img/plants/ficus.jpg', 'rb')))
        cls.plant.save()

    @classmethod
    def tearDownClass(cls):
        cls.plant.picture.delete()
        UserProfile.objects.get(user_id=cls.user_id).picture.delete()

        super().tearDownClass()

    def setUp(self):
        # create a superuser and log it in
        User.objects.create_superuser('testAdmin', 'email@email.com', 'adminPassword123')
        self.client.login(username='testAdmin', password='adminPassword123')

    def test_index_url_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_treebay_url_exists(self):
        response = self.client.get('/treebay/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_exists(self):
        response = self.client.get('/treebay/login/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_exists(self):
        response = self.client.get('/treebay/about/')
        self.assertEqual(response.status_code, 200)

    def test_show_category_uses_correct_template(self):
        response = self.client.get(reverse('treebay:show_category', kwargs={'category_name_slug': 'houseplants'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/category.html')
        self.assertTemplateUsed(response, 'treebay/base.html')

    def test_show_user_uses_correct_template(self):
        response = self.client.get(
            reverse('treebay:show_user', kwargs={'user_username': 'alice'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/show_user.html')
        self.assertTemplateUsed(response, 'treebay/base.html')

    def test_edit_user_uses_correct_template(self):
        response = self.client.get(reverse('treebay:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/edit_profile.html')
        self.assertTemplateUsed(response, 'treebay/base.html')

    def test_change_password_uses_correct_template(self):
        response = self.client.get(reverse('treebay:change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/change_password.html')

    def test_delete_profile_uses_correct_template(self):
        response = self.client.get(reverse('treebay:delete_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/delete_profile.html')

    def test_add_plant_uses_correct_template(self):
        response = self.client.get(reverse('treebay:add_plant'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/add_edit_plant.html')

    def test_show_plant_uses_correct_template(self):
        response = self.client.get(
            reverse('treebay:show_plant', kwargs={'plant_slug': 'houseplants', 'plant_id': self.plant.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/show_plant.html')

    def test_dashboard_view_exists_and_uses_correct_template(self):
        response = self.client.get(reverse('treebay:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'treebay/dashboard.html')

    def test_starred_view_exists(self):
        response = self.client.get(reverse('treebay:star'))
        self.assertEqual(response.status_code, 200)

    def test_admin_url_is_not_accessible_for_non_superusers(self):
        self.client.logout()
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
