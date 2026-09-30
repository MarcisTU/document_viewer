from enum import Enum


class ImportanceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DocumentCategory(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"


"""
Šeit mēs definējam maksimāli visus korektus failu tipus 
    (produkcijā būtu jābūt iespējai mainīt atļautos datu tipus e.g. glabāt datu bāzē un validēt API pusē)
"""
class FileType(str, Enum):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    ODT = "odt"
    RTF = "rtf"
    TXT = "txt"
    XLS = "xls"
    XLSX = "xlsx"
    ODS = "ods"
    CSV = "csv"
    PPT = "ppt"
    PPTX = "pptx"
    ODP = "odp"
    XML = "xml"
    JSON = "json"
    HTML = "html"
    HTM = "htm"
    ZIP = "zip"
    RAR = "rar"
    SEVEN_Z = "7z"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    SVG = "svg"
    WEBP = "webp"
    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
