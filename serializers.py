from abc import ABC, abstractmethod
from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json

from exceptions import BookingException



class Serializer(ABC):
    @abstractmethod
    def to_file(self, data: List[Any], filename: str) -> None:
        pass

    @abstractmethod
    def from_file(self, filename: str) -> List[Dict[str, Any]]:
        pass


class JSONSerializer(Serializer):
    def to_file(self, data: List[Any], filename: str) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([obj.to_dict() for obj in data], f, indent=2, default=str)
            print(f"Data saved to {filename}")
        except IOError as e:
            print(f"Error saving to {filename}: {e}")
            raise BookingException(f"Failed to save to {filename}: {str(e)}")
        except AttributeError:
            raise BookingException("Error: An object in the list does not have a to_dict() method.")

    def from_file(self, filename: str) -> List[Dict[str, Any]]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Data loaded from {filename}")
            return data
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading from {filename}: {e}")
            raise BookingException(f"Failed to load from {filename}: {str(e)}")


class XMLSerializer(Serializer):
    def to_file(self, data: List[Any], filename: str) -> None:
        try:
            root = ET.Element("data")
            for item in data:
                item_data = item.to_dict()
                item_name = item.__class__.__name__.lower()
                elem = ET.SubElement(root, item_name)

                def build_xml(parent_elem, dictionary):
                    for key, value in dictionary.items():
                        if isinstance(value, dict):
                            child_elem = ET.SubElement(parent_elem, key)
                            build_xml(child_elem, value)
                        elif isinstance(value, list):
                            list_elem = ET.SubElement(parent_elem, key)
                            for list_item in value:
                                if isinstance(list_item, dict):
                                    build_xml(ET.SubElement(list_elem, "item"), list_item)
                                else:
                                    ET.SubElement(list_elem, "item").text = str(list_item)
                        else:
                            child = ET.SubElement(parent_elem, key)
                            child.text = str(value)

                build_xml(elem, item_data)

            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            raise BookingException(f"Failed to save to {filename}: {str(e)}")
        except AttributeError:
            raise BookingException("Error: An object in the list does not have a to_dict() method.")

    def from_file(self, filename: str) -> List[Dict[str, Any]]:
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            data = []

            def parse_xml(element):
                parsed_dict = {}
                for child in element:
                    if len(child) == 0:
                        parsed_dict[child.tag] = child.text
                    else:
                        parsed_dict[child.tag] = parse_xml(child)
                return parsed_dict

            for item in root:
                data.append(parse_xml(item))

            print(f"Data loaded from {filename}")
            return data
        except (IOError, ET.ParseError) as e:
            print(f"Error loading from {filename}: {e}")
            raise BookingException(f"Failed to load from {filename}: {str(e)}")