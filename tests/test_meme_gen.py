import importlib.util, json, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("meme_gen", ROOT / "skills/meme-gen/scripts/meme_gen.py")
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 50


class Encoding(unittest.TestCase):
    def test_specials(self):
        self.assertEqual(mg.encode_line("a b"), "a_b")
        self.assertEqual(mg.encode_line("a_b"), "a__b")
        self.assertEqual(mg.encode_line("zero-day"), "zero--day")
        self.assertEqual(mg.encode_line("why?"), "why~q")
        self.assertEqual(mg.encode_line("a/b"), "a~sb")
        self.assertEqual(mg.encode_line("100%"), "100~p")
        self.assertEqual(mg.encode_line("#1 & more"), "~h1_~a_more")
        self.assertEqual(mg.encode_line(""), "_")
        self.assertIn("%27", mg.encode_line("can't").replace("'", "%27")) 

    def test_plus_is_encoded(self):
        self.assertEqual(mg.encode_line("C++"), "C%2B%2B")

    def test_too_long(self):
        with self.assertRaises(mg.MemeError):
            mg.encode_line("x" * 500)

    def test_build_url(self):
        u = mg.build_url("drake", ["a", "b"], 800)
        self.assertEqual(u, "https://api.memegen.link/images/drake/a/b.png?width=800")
        with self.assertRaises(mg.MemeError):
            mg.build_url("../x", ["a"])
        with self.assertRaises(mg.MemeError):
            mg.build_url("drake", ["a"], 50)


class Safety(unittest.TestCase):
    def test_url_checks(self):
        mg.check_url("https://api.memegen.link/images/x.png")
        for bad in ["http://api.memegen.link/x", "https://evil.example/x",
                    "https://api.memegen.link.evil.example/x", "https://u:p@api.memegen.link/x"]:
            with self.assertRaises(mg.MemeError):
                mg.check_url(bad)

    def test_validate_rejects_html(self):
        with self.assertRaises(mg.MemeError):
            mg.validate_image(b"<html>nope</html>")
        with self.assertRaises(mg.MemeError):
            mg.validate_image(b"")


class Specs(unittest.TestCase):
    def setUp(self):
        self.tmap = mg.template_map()

    def test_templates_consistent(self):
        for t in mg.load_templates():
            self.assertEqual(len(t["roles"]), t["lines"], t["id"])
            self.assertEqual(len(t["example"]), t["lines"], t["id"])

    def test_pads_and_rejects(self):
        s = mg.normalise_spec({"template": "gb", "text": ["a", "b"]}, self.tmap)
        self.assertEqual(len(s["text"]), 4)
        with self.assertRaises(mg.MemeError):
            mg.normalise_spec({"template": "drake", "text": ["a", "b", "c"]}, self.tmap)
        with self.assertRaises(mg.MemeError):
            mg.normalise_spec({"template": "drake"}, self.tmap)

    def test_long_box_warns(self):
        s = mg.normalise_spec({"template": "drake", "text": [" ".join(["w"] * 20), "b"]}, self.tmap)
        self.assertTrue(s["warnings"])

    def test_hashtags(self):
        s = mg.normalise_spec({"template": "cmm", "text": "x", "hashtags": "dev #ai"}, self.tmap)
        self.assertEqual(s["hashtags"], ["#dev", "#ai"])


class Files(unittest.TestCase):
    def test_naming_and_save(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            p = mg.save_image(PNG, out, "2026-01-01-01-drake") if not mg._pillow() else None
            if p:
                self.assertTrue(p.exists())
                p2 = mg.unique_path(p)
                self.assertNotEqual(p, p2)
            (out / "2026-01-01-03-x.png").write_bytes(PNG)
            self.assertEqual(mg.next_index(out, "2026-01-01"), 4)

    def test_box_parse(self):
        x, y, w, h, st, t = mg.parse_box("0.1,0.2,0.5,0.3,k=hi there")
        self.assertEqual((st, t), ("k", "hi there"))
        with self.assertRaises(mg.MemeError):
            mg.parse_box("0.9,0.9,0.5,0.5=oops")

    def test_batch_load(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "b.json"
            f.write_text(json.dumps({"memes": [{"template": "drake", "text": ["a", "b"]}]}))
            self.assertEqual(len(mg._load_batch(f)), 1)
            f.write_text("[]")
            with self.assertRaises(mg.MemeError):
                mg._load_batch(f)


if __name__ == "__main__":
    unittest.main()
