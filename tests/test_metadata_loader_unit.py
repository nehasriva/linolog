"""Unit tests for MetadataLoader."""

import yaml
from linolog.metadata_loader import MetadataLoader


class TestExtractFromFolderName:
    def setup_method(self):
        self.loader = MetadataLoader()

    def test_with_edition(self):
        result = self.loader._extract_from_folder_name("sunset_edition_3")
        assert result["title"] == "Sunset"
        assert result["edition"] == "3"

    def test_with_edition_and_extra_info(self):
        result = self.loader._extract_from_folder_name("sunset_edition_3_8x10")
        assert result["title"] == "Sunset"
        assert result["edition"] == "3"
        assert result["size"] == "8x10"

    def test_without_edition(self):
        result = self.loader._extract_from_folder_name("random_folder")
        assert result == {}

    def test_multi_word_title(self):
        result = self.loader._extract_from_folder_name("ocean_waves_edition_2")
        assert result["title"] == "Ocean Waves"
        assert result["edition"] == "2"


class TestLoadYamlMetadata:
    def setup_method(self):
        self.loader = MetadataLoader()

    def test_valid_yaml(self, tmp_path):
        yaml_file = tmp_path / "metadata.yaml"
        yaml_file.write_text("title: Sunset\nedition: '3'\n")
        result = self.loader._load_yaml_metadata(str(yaml_file))
        assert result["title"] == "Sunset"
        assert result["edition"] == "3"

    def test_invalid_yaml(self, tmp_path):
        yaml_file = tmp_path / "metadata.yaml"
        yaml_file.write_text("invalid: [yaml: {broken")
        result = self.loader._load_yaml_metadata(str(yaml_file))
        assert result == {}

    def test_empty_file(self, tmp_path):
        yaml_file = tmp_path / "metadata.yaml"
        yaml_file.write_text("")
        result = self.loader._load_yaml_metadata(str(yaml_file))
        assert result == {}


class TestLoadMetadata:
    def setup_method(self):
        self.loader = MetadataLoader()

    def test_with_yaml_file(self, tmp_path):
        yaml_file = tmp_path / "metadata.yaml"
        yaml_file.write_text("title: Sunset\nedition: '3'\n")
        result = self.loader.load_metadata(str(tmp_path))
        assert result["title"] == "Sunset"
        assert "date" in result  # Should add date

    def test_without_yaml_uses_folder_name(self, tmp_path):
        # tmp_path won't have metadata.yaml, so it extracts from folder name
        result = self.loader.load_metadata(str(tmp_path))
        assert "date" in result

    def test_adds_date_if_missing(self, tmp_path):
        yaml_file = tmp_path / "metadata.yaml"
        yaml_file.write_text("title: Test\n")
        result = self.loader.load_metadata(str(tmp_path))
        assert "date" in result

    def test_preserves_existing_date(self, tmp_path):
        yaml_file = tmp_path / "metadata.yaml"
        yaml_file.write_text("title: Test\ndate: '2024-01-01'\n")
        result = self.loader.load_metadata(str(tmp_path))
        assert result["date"] == "2024-01-01"


class TestSaveMetadata:
    def setup_method(self):
        self.loader = MetadataLoader()

    def test_saves_valid_yaml(self, tmp_path):
        metadata = {"title": "Sunset", "edition": "3"}
        result = self.loader.save_metadata(str(tmp_path), metadata)
        assert result is True

        saved = yaml.safe_load((tmp_path / "metadata.yaml").read_text())
        assert saved["title"] == "Sunset"

    def test_returns_false_on_error(self):
        result = self.loader.save_metadata("/nonexistent/path", {"title": "Test"})
        assert result is False


class TestGetPrintImagePath:
    def setup_method(self):
        self.loader = MetadataLoader()

    def test_prefers_final(self, tmp_path):
        (tmp_path / "random.jpg").touch()
        (tmp_path / "final_print.jpg").touch()
        result = self.loader.get_print_image_path(str(tmp_path))
        assert "final_print.jpg" in result

    def test_falls_back_to_first(self, tmp_path):
        (tmp_path / "photo.png").touch()
        result = self.loader.get_print_image_path(str(tmp_path))
        assert "photo.png" in result

    def test_no_images(self, tmp_path):
        (tmp_path / "notes.txt").touch()
        result = self.loader.get_print_image_path(str(tmp_path))
        assert result is None
