import unittest
from formato_video import FormatoVideo


class TestFormatoVideo(unittest.TestCase):
    def test_mime_valido(self):
        self.assertEqual(FormatoVideo.from_mime("video/mp4"), "mp4")
        self.assertEqual(FormatoVideo.from_mime("video/x-msvideo"), "avi")
        self.assertEqual(FormatoVideo.from_mime("video/x-matroska"), "mkv")
        self.assertEqual(FormatoVideo.from_mime("video/quicktime"), "mov")
        self.assertEqual(FormatoVideo.from_mime("video/x-ms-wmv"), "wmv")
        self.assertEqual(FormatoVideo.from_mime("video/x-flv"), "flv")
        self.assertEqual(FormatoVideo.from_mime("video/webm"), "webm")
        self.assertEqual(FormatoVideo.from_mime("video/mpeg"), "mpeg")
        self.assertEqual(FormatoVideo.from_mime("video/ogg"), "ogg")

    def test_mime_invalido(self):
        self.assertIsNone(FormatoVideo.from_mime("video/unknown"))
        self.assertIsNone(FormatoVideo.from_mime("audio/mp3"))
        self.assertIsNone(FormatoVideo.from_mime(""))
        self.assertIsNone(FormatoVideo.from_mime(None))

    def test_valores_enum(self):
        self.assertEqual(FormatoVideo.MP4.value, "video/mp4")
        self.assertEqual(FormatoVideo.AVI.value, "video/x-msvideo")
        self.assertEqual(FormatoVideo.MKV.value, "video/x-matroska")
        self.assertEqual(FormatoVideo.MOV.value, "video/quicktime")
        self.assertEqual(FormatoVideo.WMV.value, "video/x-ms-wmv")
        self.assertEqual(FormatoVideo.FLV.value, "video/x-flv")
        self.assertEqual(FormatoVideo.WEBM.value, "video/webm")
        self.assertEqual(FormatoVideo.MPEG.value, "video/mpeg")
        self.assertEqual(FormatoVideo.OGG.value, "video/ogg")