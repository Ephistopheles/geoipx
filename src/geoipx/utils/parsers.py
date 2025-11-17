import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv
from io import StringIO

def to_json(data: dict) -> str:
    return json.dumps(data, indent=4)

def to_xml(data: dict) -> str:
    root = ET.Element("GeoIPX")
    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)

    xml_str = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

    return pretty_xml.strip()

def to_csv(data: dict) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)
    return output.getvalue()
