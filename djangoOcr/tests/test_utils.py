from django.test import SimpleTestCase
from djangoOcr.utils import fix_unicode, write_output_to_file, read_text_from_file, apply_ocr, remove_spaces
from djangoOcr.views import convert_image_to_text

class TestUtils(SimpleTestCase):

    def test_fix_unicode_returns_correct_result(self):
        text = fix_unicode('uÌˆnicode')
        self.assertEquals("ünicode", text)

    def test_write_output_to_file(self):
        filename = 'test_write_output.txt'
        write_output_to_file('hello world', filename)
        file = open(filename, 'r', encoding='utf-8')
        text = file.read()
        self.assertNotEquals("Hello World", text)
        self.assertEquals("hello world", text)    

    def test_read_text_from_unknown_file(self):
        filename = 'test_write_output.txt'
        res = read_text_from_file(filename)
        self.assertEquals("hello world", res)

    def test_remove_spaces(self):
        formatted_list = read_text_from_file('test_output.txt')  
        formatted_list = list(filter(None, remove_spaces(formatted_list)))
        self.assertEquals(6, len(formatted_list))

    def test_remove_spaces_if_empty(self):
        formatted_list = list(filter(None, remove_spaces("")))
        self.assertEquals(0, len(formatted_list)) 

    def test_remove_spaces_returns_correct_output(self):
        formatted_list = read_text_from_file('test_output.txt')  
        formatted_list = list(filter(None, remove_spaces(formatted_list)))
        self.assertEquals("but also the lead", formatted_list[2])
        self.assertEquals(False, '' in formatted_list)

    def test_convert_image_to_test(self):
        file = "this is a sample test image.pdf"
        result = convert_image_to_text(file)
        self.assertEquals("", result)
        self.assertEquals("", convert_image_to_text(""))                 
