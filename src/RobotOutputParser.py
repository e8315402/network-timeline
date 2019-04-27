#!/usr/bin/python3

import json
import xml.etree.ElementTree as ET

class RobotOutputParser():
    def __init__(self):
        self.robot_output_file = None

    def set_robot_output_file(self, output):
        self.robot_output_file = output

    def parse_to_node_tree(self):
        return ET.parse(self.robot_output_file).getroot()

    def parse_output(self):
        node_tree = self.parse_to_node_tree()
        return self.parse_keyword(node_tree)

    def parse_keyword(self, kw):
        kw_status = kw.find('status')
        kw_info = {
            'name': kw.attrib.get('name'),
            'status': kw_status.attrib.get('status'),
            'starttime': kw_status.attrib.get('starttime'),
            'endtime': kw_status.attrib.get('endtime')
        }
        kw_children = kw.findall('kw')
        if len(kw_children) != 0:
            kw_info['keywords'] = [self.parse_keyword(
                kw_child) for kw_child in kw_children]
        return kw_info
    
    def parse_output_and_save_to(self, target_path):
        keywords = self.parse_output()
        with open(target_path, 'w') as f:
            json.dump(keywords, f)