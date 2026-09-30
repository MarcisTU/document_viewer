import asyncio
from random import choice, randint
import xml.etree.ElementTree as ET

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from faker import Faker

from dependencies.database import engine
from models.db import Document, DocumentCreate
from models.enums import DocumentCategory, FileType, ImportanceLevel


fake = Faker()

# Pieņemot dažas gadījuma vērtības
RESPONSIBLE_UNITS = [
    "Finance Department",
    "Human Resources",
    "IT Department",
    "Legal Department",
    "Marketing Department",
    "Operations Department",
]


def generate_documents(count: int = 10) -> list[DocumentCreate]:
    documents: list[DocumentCreate] = []

    for _ in range(count):
        file_type = choice(list(FileType))

        document = DocumentCreate(
            name=fake.sentence(nb_words=5).rstrip("."),
            description=fake.paragraph(nb_sentences=2),
            responsible_unit=choice(RESPONSIBLE_UNITS),
            creation_date=fake.date_between(
                start_date="-2y",
                end_date="today",
            ),
            url=f"https://example.com/documents/{fake.uuid4()}{file_type.value}",
            file_type=file_type,
            reading_time_minutes=randint(1, 120),
            importance=choice(list(ImportanceLevel)),
            category=choice(list(DocumentCategory)),
            is_active=choice([True, False]),
        )

        documents.append(document)

    return documents


async def fetch_remote_xml() -> bytes:
    """
    Simulējam attālinātu http izsaukumu, kurš atgrieztu XML datus
    """

    # izveido nejaušinātus xml dokumenta datus, izmantojot izveidoto pydantic datu modeli
    documents = generate_documents(10)

    root = ET.Element("documents")

    for document in documents:
        document_element = ET.SubElement(root, "document")

        data = document.model_dump(mode="json")

        for field_name, value in data.items():
            element = ET.SubElement(document_element, field_name)
            element.text = str(value).lower() if isinstance(value, bool) else str(value)

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True,
    )


def parse_documents_xml(xml_data: bytes) -> list[DocumentCreate]:
    """
    Pārveido simulētos datus uz API dokumenta struktūru izmantojot definētos atribūtus un validējot datus
    """

    root = ET.fromstring(xml_data)

    documents: list[DocumentCreate] = []

    for element in root.findall("document"):
        data = {
            field_name: element.findtext(field_name)
            for field_name in DocumentCreate.model_fields
        }

        data["reading_time_minutes"] = int(data["reading_time_minutes"])
        data["is_active"] = data["is_active"].lower() == "true"

        document = DocumentCreate.model_validate(data)
        documents.append(document)

    return documents


async def seed_documents(
    session: AsyncSession,
):
    result = await session.exec(
        select(Document).limit(1)
    )
    existing_document = result.first()

    if existing_document is not None:
        print("Documents already exist in the database. Skipping adding more data.")
        return

    xml_data = await fetch_remote_xml()

    imported_documents = parse_documents_xml(xml_data)

    documents = []
    for document in imported_documents:
        document_data = document.model_dump()
        # Convert from HttpUrl to str format explicitly
        document_data["url"] = str(document.url)
        documents.append(Document(**document_data))

    session.add_all(documents)
    await session.commit()


async def main() -> None:
    async with AsyncSession(engine) as session:
        await seed_documents(session)


if __name__ == "__main__":
    asyncio.run(main())
