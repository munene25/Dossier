import os
import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from .models import ResumeModel
from .forms import ResumeForm

TEMP_MEDIA_ROOT = tempfile.mkdtemp()
@override_settings(MEDIA_ROOT = TEMP_MEDIA_ROOT)
class ResumeTests(TestCase):
    @staticmethod
    def create_dummy_pdf(content_type):
        return SimpleUploadedFile('test_resume.pdf', b"dummy_content", content_type=content_type)

    def test_resume_form_with_valid_file(self):
        '''test if the form returns true for a valid file format'''
        form = ResumeForm(data={}, files={'pdf_file':self.create_dummy_pdf('application/pdf')})
        self.assertTrue(form.is_valid(), 'form with valid file returned False')
    
    def test_resume_form_with_invalid_file(self):
        '''with invalid text file, check if the form validation returns false'''
        form = ResumeForm(data={}, files={'pdf_file': self.create_dummy_pdf('text/plain')})  # Use the stored file
        self.assertFalse(form.is_valid(), 'form with invalid file returned True')
    
    def test_resume_model_with_valid_file(self):
        '''Unit test for model with dummy file'''
        ResumeModel.objects.create(pdf_file=self.create_dummy_pdf('application/pdf'))
        self.assertEqual(ResumeModel.objects.count(),1)
    
    def test_upload_valid_pdf(self):
        '''end to end client test for checking if model saves data if valid form is submitted'''
        client = Client()
        pdf_path = os.path.join(settings.BASE_DIR, 'resumes', 'tests', 'test_resume.pdf')

        self.assertTrue(os.path.exists(pdf_path), "Test PDF file is missing")

        with open(pdf_path, 'rb') as pdf_file:
             response = client.post(
                  '/resumes/',
                  data = {'pdf_file':pdf_file},
                )
        self.assertEqual(response.status_code, 302, 'Redirect did not occur')
        self.assertEqual(ResumeModel.objects.count(),1)
    
    def test_upload_invalid_pdf(self):
        '''end to end client test for checking whether the file a user '''
        client = Client()
        form = ResumeForm(data={}, files={'pdf_file': self.create_dummy_pdf('text/plain')})

        client.post('/resumes/',{'pdf_file':form})
        self.assertEqual(ResumeModel.objects.count(),0)

    def tearDown(self):
        '''delete all files after test runs'''
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDown() # call the parentclass teardown method