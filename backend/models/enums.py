from enum import Enum


"""
Visas kategoriskās vērtības atribūtu nosaukumus iekš programmatūras standartizē uz angļu valodu 
"""
class ImportanceLevel(str, Enum):
    LOW = "zems"
    MEDIUM = "vidējs"
    HIGH = "augsts"
    CRITICAL = "kritisks"


class DocumentCategory(str, Enum):
    PUBLIC = "publisks"
    INTERNAL = "iekšējs"
    RESTRICTED = "ierobežotas pieejamības"
    CONFIDENTIAL = "konfidenciāls"


class ActiveStatus(str, Enum):
    YES = "jā"
    NO = "nē"


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
