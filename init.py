import os
import unittest
import xml.etree.ElementTree as ET

class test_robot_output_parser(unittest.TestCase):
    
    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
    
    def test_construction(self):
        rop = RobotOutputParser()
        self.assertIsInstance(rop, RobotOutputParser)
    
    def test_set_robot_output_file(self):
        mock_robot_output_file_path = os.path.join(self.current_dir, 'fixture', 'set_robot_output_file.xml')
        rop = RobotOutputParser()
        rop.set_robot_output_file(mock_robot_output_file_path)
        self.assertEqual(rop.robot_output_file, mock_robot_output_file_path)

    def test_parse_output(self):
        mock_robot_output_file_path = os.path.join(self.current_dir, 'fixture', 'parse_output.xml')
        rop = RobotOutputParser()
        rop.set_robot_output_file(mock_robot_output_file_path)
        actual_keyowrd_info = rop.parse_output()
        expect_keyword_info = {
            'name': 'Login',
            'status': 'PASS',
            'starttime': '20190423 13:11:24.102',
            'endtime': '20190423 13:11:27.807'
        }
        self.assertEqual(actual_keyowrd_info, expect_keyword_info)


    def test_extract_keyword_info__single_keyword(self):
        mock_keyword_string = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <kw name="Login">
                <status status="PASS" starttime="20190423 13:11:24.102" endtime="20190423 13:11:27.807"></status>
            </kw>
        '''
        output_tree = ET.fromstring(mock_keyword_string)
        expect_keyword_info = {
            'name': 'Login',
            'status': 'PASS',
            'starttime': '20190423 13:11:24.102',
            'endtime': '20190423 13:11:27.807'
        }
        rop = RobotOutputParser()
        actual_keyowrd_info = rop.extract_keyword_info(mock_keyword)
        self.assertEqual(actual_keyowrd_info, expect_keyword_info)

    # def test_extract_keyword_info__one_keyword_contains_one_keyword(self):
    #     mock_keywords = '''
    #         <kw name="Login">
    #             <kw name="Close Browser" library="SeleniumLibrary">
    #     		    <status status="PASS" starttime="20190423 13:11:35.912" endtime="20190423 13:11:37.968"></status>
	#             </kw>
    #             <status status="PASS" starttime="20190423 13:11:24.102" endtime="20190423 13:11:27.807"></status>
    #         </kw>
    #     '''
    #     expect_keyword_info = {
    #         'name': 'Login',
    #         'status': 'PASS',
    #         'starttime': '20190423 13:11:24.102',
    #         'endtime': '20190423 13:11:27.807',
    #         'keywords': [
    #             {
    #                 'name': 'Close Browser',
    #                 'status': 'PASS',
    #                 'starttime': '20190423 13:11:35.912',
    #                 'endtime': '20190423 13:11:37.968'
    #             }
    #         ]
    #     }
    #     rop = RobotOutputParser()
    #     actual_keyowrd_info = rop.extract_keyword_info(mock_keywords)
    #     self.assertEqual(actual_keyowrd_info, expect_keyword_info)

class RobotOutputParser():
    def __init__(self):
        self.robot_output_file = None
    
    def set_robot_output_file(self, output):
        self.robot_output_file = output

    def parse_output(self):
        return ET.parse(self.robot_output_file).getroot()

    def extract_keyword_info(self, kw_xml):
        kw = ET.fromstring(kw_xml)
        kw_status = kw.find('./status')
        kw_info = {
            'name': kw.attrib.get('name'),
            'status': kw_status.attrib.get('status'),
            'starttime': kw_status.attrib.get('starttime'),
            'endtime': kw_status.attrib.get('endtime')
        }
        sub_kw = kw.find('kw')
        if sub_kw:
            sub_kw_info = self.extract_keyword_info(sub_kw)
            kw_info['keywords'] = [sub_kw_info]
        return kw_info

if __name__ == "__main__":
    unittest.main()


