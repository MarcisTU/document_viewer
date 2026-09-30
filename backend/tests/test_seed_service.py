import xml.etree.ElementTree as ET

from data.seed_service import parse_documents_xml


def test_parse_documents_xml():
    xml_data = b"""<?xml version="1.0" encoding="utf-8"?>
    <documents>
        <document>
            <name>Test document</name>
            <description>Test description</description>
            <responsible_unit>IT Department</responsible_unit>
            <creation_date>2026-09-30</creation_date>
            <url>https://example.com/document.pdf</url>
            <file_type>pdf</file_type>
            <reading_time_minutes>10</reading_time_minutes>
            <importance>high</importance>
            <category>internal</category>
            <is_active>true</is_active>
        </document>
    </documents>
    """

    documents = parse_documents_xml(xml_data)

    assert len(documents) == 1

    document = documents[0]

    assert document.name == "Test document"
    assert document.responsible_unit == "IT Department"
    assert document.reading_time_minutes == 10
    assert document.is_active is True
    assert str(document.url) == "https://example.com/document.pdf"
