# -*- coding:utf-8 -*-

import xml.etree.ElementTree as ET
import json
import os
import sys


data_id = 1
tree = ET.ElementTree()

class XmlEdit:
    def __init__(self):
        pass

     # 遍历xml节点
    def through_xml_data(self, root_node, level, result_list):
        global data_id
        temp_list = [data_id, level, root_node.tag, root_node.attrib]
        result_list.append(temp_list)
        data_id += 1

        # 遍历每个子节点
        children_node = root_node.getchildren()
        if len(children_node) == 0:
            return
        for child in children_node:
            self.through_xml_data(child, level + 1, result_list)
        return


    # 获取xml文件
    def get_xml_file(self, in_file_path):
        if os.path.exists(in_file_path):
            print "xml file:" + in_file_path + " exit"
            root = ET.parse(in_file_path).getroot()
            level = 1
            result_list = []
            self.through_xml_data(root, level, result_list)
            return result_list
        else:
            print "xml file" + in_file_path + " no exit"
            return []


    # 当key处于isdbt中属性相同的数据部分,获取分别对应的位置
    def get_isdbt_same_attr_positon(self, key, result_list):
        # layer对应在result_list中的位置
        map_dict = {"layer1": 3, "Layer1": 3,
                    "layer2": 4, "Layer2": 4,
                    "layer3": 5, "Layer5": 5,
                    "layera": 7, "layerA": 7,
                    "layerb": 8, "layerB": 8,
                    "layerc": 9, "layerC":9}
        if key in map_dict.keys():
            position = map_dict[key]
            result = result_list[position]
            return True, result, position
        else:
            return False, " ", 0


    # 修改xml项值,默认一个值，只有当tag_name = layer时，修改该参数
    def update_xml_data(self, root, tag_name, attrib_name, value, flag = 9):
        if tag_name == "Layer":
            find_num = 0
            # 当tag_name 是Layer（会全部修改），以后再实现
            for child in root.iter(tag_name):
                find_num += 1
                if find_num == flag:
                    child.attrib[attrib_name] = value
                    print "update xml config:" + attrib_name + " of " + tag_name
        else:
            for child in root.iter(tag_name):
                child.attrib[attrib_name] = value
                print "update xml config:" + attrib_name + " of " + tag_name


    #解析配置文件
    def load_xml_edit_config(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                xml_config = json.load(f)
                return xml_config
        else:
            print "error:" + filepath + ' no exit'
            return


    # 解析配置文件字典，获取想要编译的xml,xml_file_name为文件名，xml_config为整个配置文件
    def parse_xml_config(self, xml_file_name, xml_config):
        if xml_file_name in xml_config.keys():
            xml_config_data = xml_config[xml_file_name]
            print "edit:" + xml_file_name
            return True, xml_config_data
        else:
            print "error:" + xml_file_name + " no exit"
            return False, {}


    # 判断ts_config_data中的key是否在xml中，存在的话，修改值，并输出xml配置文档，码流机打开新配置文件
    def exist_and_replace(self, xml_config_data, root, ret_list, f_type='t2'):
        for key in xml_config_data.keys():
            flag = False
            if f_type == "isdbt":
                ret, result, position = self.get_isdbt_same_attr_positon(key, ret_list)
                if ret:
                    flag = True
                    same_attr_dict = xml_config_data[key]
                    layer_dict = {3: 1, 4: 2, 5: 3}
                    # 处于layer1-3
                    if position in [3, 4, 5]:
                        for same_attr_key in same_attr_dict.keys():
                            same_attr_key_flag = False
                            if same_attr_key in result[3].keys():
                                same_attr_key_flag = True
                                self.update_xml_data(root, result[2], same_attr_key, same_attr_dict[same_attr_key], layer_dict[position])
                            if not same_attr_key_flag:
                                print same_attr_key + " no exit in config file"
                    else:
                        for same_attr_key in same_attr_dict.keys():
                            same_attr_key_flag = False
                            if same_attr_key in result[3].keys():
                                same_attr_key_flag = True
                                self.update_xml_data(root, result[2], same_attr_key, same_attr_dict[same_attr_key])
                            if not same_attr_key_flag:
                                print same_attr_key + " no exit in config file"
                # 不处于Layer1-3,Layer:a-c
                else:
                    for result in ret_list:
                        if key in result[3].keys():
                            flag = True
                            self.update_xml_data(root, result[2], key, xml_config_data[key])
            else:
                for result in ret_list:
                    if key in result[3].keys():
                        flag = True
                        self.update_xml_data(root, result[2], key, xml_config_data[key])
            # 如果没匹配到，输出如下：
            if not flag:
                print "error:" + key + " no exists in xml config"


    '''
    # 单个配置名修改
    def set_xml_config(ts_type, xml_path):
        exit_flag = False
        if ts_type in ["t2", "isdbt"]:
            xml_file_path = r"./config/" + ts_type + ".json"
        else:
            print ts_type + "error"
            sys.exit(2)
    
        # 获取配置文件
        xml_config = load_xml_edit_config(xml_file_path)
        exist_and_replace(xml_config[xml_path], ts_type)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    '''


    # ts_name 为码流文件路径名称
    def set_xml_config(self, ts_type, xml_path=["all"]):
        if ts_type == "t2":
            in_file_path = "./xml_file/t2_def.xml"
            xml_file_path = r"./config/" + ts_type + ".json"
        elif ts_type == "isdbt":
            in_file_path = "./xml_file/isdbt_def.xml"
            xml_file_path = r"./config/" + ts_type + ".json"
        else:
            print "error:" + ts_type + ' is error, type should be in ["t2","isdbt"]'
            sys.exit(1)
        global tree
        # 解析原始的xml配置文件
        ret_list = self.get_xml_file(in_file_path)
        tree.parse(in_file_path)
        root = tree.getroot()

        # 获取配置文件
        xml_config = self.load_xml_edit_config(xml_file_path)
        if xml_path[0] == "all":
            for key in xml_config.keys():
                print "edit to" + key
                self.exist_and_replace(xml_config[key], root, ret_list, ts_type)
                tree.write(key, encoding="utf-8", xml_declaration=True)
        else:
            for lst in xml_path:
                ret, xml_config_data = self.parse_xml_config(lst, xml_config)
                if ret:
                    self.exist_and_replace(xml_config_data, root, ret_list, ts_type)
                tree.write(lst, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    xml = XmlEdit()
    xml.set_xml_config('isdbt')
    xml.set_xml_config('t2')