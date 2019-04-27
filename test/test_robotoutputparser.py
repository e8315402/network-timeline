#!/usr/bin/python3

import os
import json
import unittest
import xml.etree.ElementTree as ET
from src.RobotOutputParser import RobotOutputParser

class TestRobotOutputParser(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def test_construction(self):
        rop = RobotOutputParser()
        self.assertIsInstance(rop, RobotOutputParser)

    def test_set_robot_output_file(self):
        mock_robot_output_file_path = os.path.join(
            self.current_dir, 'fixture', 'set_robot_output_file.xml')
        rop = RobotOutputParser()
        rop.set_robot_output_file(mock_robot_output_file_path)
        self.assertEqual(rop.robot_output_file, mock_robot_output_file_path)

    def test_parse_output_to_keyword_info_json(self):
        mock_robot_output_file_path = os.path.join(
            self.current_dir, 'fixture', 'single_keyword.xml')
        rop = RobotOutputParser()
        rop.set_robot_output_file(mock_robot_output_file_path)
        keyword_info = rop.parse_output()
        expect_keyword_info = {
            'name': 'Login',
            'status': 'PASS',
            'starttime': '20190423 13:11:24.102',
            'endtime': '20190423 13:11:27.807'
        }
        self.assertEqual(keyword_info, expect_keyword_info)

    def test_parse_output_to_node_tree(self):
        mock_robot_output_file_path = os.path.join(
            self.current_dir, 'fixture', 'single_keyword.xml')
        rop = RobotOutputParser()
        rop.set_robot_output_file(mock_robot_output_file_path)
        node_tree = rop.parse_to_node_tree()
        self.assertIsInstance(node_tree, ET.Element)

    def test_parse_output__one_keyword_contains_another_keyword(self):
        mock_robot_output_file_path = os.path.join(
            self.current_dir, 'fixture', 'one_keyword_contains_one_keyword.xml')
        rop = RobotOutputParser()
        rop.set_robot_output_file(mock_robot_output_file_path)
        keyword_info = rop.parse_output()
        expect_keyword_info = {
            'name': 'Logoff',
            'status': 'PASS',
            'starttime': '20190423 13:11:35.693',
            'endtime': '20190423 13:11:37.970',
            'keywords': [
                    {
                        'name': 'Close Browser',
                        'status': 'PASS',
                        'starttime': '20190423 13:11:35.912',
                        'endtime': '20190423 13:11:37.968'
                    }
            ]
        }
        self.assertEqual(keyword_info, expect_keyword_info)

    def test_parse_keyword__single_keyword(self):
        single_keyword = '''<?xml version="1.0" encoding="UTF-8"?>
            <kw name="Logoff">
                <status status="PASS" 
                 starttime="20190423 13:11:35.693" 
                 endtime="20190423 13:11:37.970"></status>
            </kw>
        '''
        node_tree = ET.fromstring(single_keyword)
        rop = RobotOutputParser()
        keyword_info = rop.parse_keyword(node_tree)
        expect_keyword_info = {
            'name': 'Logoff',
            'status': 'PASS',
            'starttime': '20190423 13:11:35.693',
            'endtime': '20190423 13:11:37.970',
        }
        self.assertEqual(keyword_info, expect_keyword_info)

    def test_parse_keyword__one_keyword_contains_another_keyword(self):
        keywords = '''<?xml version="1.0" encoding="UTF-8"?>
            <kw name="Logoff">
                <kw name="Close Browser">
                    <status status="PASS" starttime="20190423 13:11:35.912" endtime="20190423 13:11:37.968"></status>
                </kw>
                <status status="PASS" starttime="20190423 13:11:35.693" endtime="20190423 13:11:37.970"></status>
            </kw>
        '''
        node_tree = ET.fromstring(keywords)
        rop = RobotOutputParser()
        keyword_info = rop.parse_keyword(node_tree)
        expect_keyword_info = {
            'name': 'Logoff',
            'status': 'PASS',
            'starttime': '20190423 13:11:35.693',
            'endtime': '20190423 13:11:37.970',
            'keywords': [
                {
                    'name': 'Close Browser',
                    'status': 'PASS',
                    'starttime': '20190423 13:11:35.912',
                    'endtime': '20190423 13:11:37.968',
                }
            ]
        }
        self.assertEqual(keyword_info, expect_keyword_info)

    def test_parse_keyword__one_keyword_contains_nest_keywords(self):
        keywords = '''<?xml version="1.0" encoding="UTF-8"?>
            <kw name="Logoff">
                <kw name="Close Browser">
                    <kw name="Log">
                        <status status="PASS" starttime="20190423 11:11:24.333" endtime="20190423 11:45:12.999"></status>
                    </kw>
                    <status status="PASS" starttime="20190423 13:11:35.912" endtime="20190423 13:11:37.968"></status>
                </kw>
                <status status="PASS" starttime="20190423 13:11:35.693" endtime="20190423 13:11:37.970"></status>
            </kw>
        '''
        node_tree = ET.fromstring(keywords)
        rop = RobotOutputParser()
        keyword_info = rop.parse_keyword(node_tree)
        expect_keyword_info = {
            'name': 'Logoff',
            'status': 'PASS',
            'starttime': '20190423 13:11:35.693',
            'endtime': '20190423 13:11:37.970',
            'keywords': [
                {
                    'name': 'Close Browser',
                    'status': 'PASS',
                    'starttime': '20190423 13:11:35.912',
                    'endtime': '20190423 13:11:37.968',
                    'keywords': [
                        {
                            'name': 'Log',
                            'status': 'PASS',
                            'starttime': '20190423 11:11:24.333',
                            'endtime': '20190423 11:45:12.999',
                        }
                    ]
                }
            ]
        }
        self.assertEqual(keyword_info, expect_keyword_info)

    def test_parse_keyword__one_keyword_contains_several_keywords(self):
        keywords = '''<?xml version="1.0" encoding="UTF-8"?>
            <kw name="Logoff">
                <kw name="Close Browser">
                    <status status="PASS" starttime="20190423 13:11:35.912" endtime="20190423 13:11:37.968"></status>
                </kw>
                <kw name="Log">
                        <status status="PASS" starttime="20190423 11:11:24.333" endtime="20190423 11:45:12.999"></status>
                    </kw>
                <status status="PASS" starttime="20190423 13:11:35.693" endtime="20190423 13:11:37.970"></status>
            </kw>
        '''
        node_tree = ET.fromstring(keywords)
        rop = RobotOutputParser()
        keyword_info = rop.parse_keyword(node_tree)
        expect_keyword_info = {
            'name': 'Logoff',
            'status': 'PASS',
            'starttime': '20190423 13:11:35.693',
            'endtime': '20190423 13:11:37.970',
            'keywords': [
                {
                    'name': 'Close Browser',
                    'status': 'PASS',
                    'starttime': '20190423 13:11:35.912',
                    'endtime': '20190423 13:11:37.968',
                },
                {
                    'name': 'Log',
                    'status': 'PASS',
                    'starttime': '20190423 11:11:24.333',
                    'endtime': '20190423 11:45:12.999',
                }
            ]
        }
        self.assertEqual(keyword_info, expect_keyword_info)

    def test_parse_output_and_save_to(self):
        mock_robot_output_file_path = os.path.join(
            self.current_dir, 'fixture', 'single_keyword.xml')
        rop = RobotOutputParser()
        rop.set_robot_output_file(mock_robot_output_file_path)
        rop.parse_output_and_save_to('keywords.json')
        expect_keyword_info = {
            'name': 'Login',
            'status': 'PASS',
            'starttime': '20190423 13:11:24.102',
            'endtime': '20190423 13:11:27.807'
        }
        with open('keywords.json', 'r') as f:
            keywords = json.load(f)
            self.assertEqual(keywords, expect_keyword_info)
            os.remove('keywords.json')
