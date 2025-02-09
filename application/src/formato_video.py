from enum import Enum


class FormatoVideo(Enum):
    MP4 = "video/mp4"
    AVI = "video/x-msvideo"
    MKV = "video/x-matroska"
    MOV = "video/quicktime"
    WMV = "video/x-ms-wmv"
    FLV = "video/x-flv"
    WEBM = "video/webm"
    MPEG = "video/mpeg"
    OGG = "video/ogg"

    @classmethod
    def from_mime(cls, mime_type: str):
        for format in cls:
            if format.value == mime_type:
                return format.name.lower()
        return None
