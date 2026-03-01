"""Unit tests for TagAgent."""

from linolog.agents.tag_agent import TagAgent


class TestExtractTextContent:
    def setup_method(self):
        self.agent = TagAgent()

    def test_strings(self):
        metadata = {"title": "Sunset", "medium": "Linocut"}
        result = self.agent._extract_text_content(metadata)
        assert "sunset" in result
        assert "linocut" in result

    def test_lists(self):
        metadata = {"colors_used": ["red", "blue"]}
        result = self.agent._extract_text_content(metadata)
        assert "red" in result
        assert "blue" in result

    def test_none_values_skipped(self):
        metadata = {"title": None, "medium": "Linocut"}
        result = self.agent._extract_text_content(metadata)
        assert "linocut" in result

    def test_numeric_values(self):
        metadata = {"blocks_used": 3}
        result = self.agent._extract_text_content(metadata)
        assert "3" in result


class TestMatchesKeywords:
    def setup_method(self):
        self.agent = TagAgent()

    def test_found(self):
        assert self.agent._matches_keywords("a landscape painting", ["landscape"])

    def test_not_found(self):
        assert not self.agent._matches_keywords("a still life", ["landscape"])


class TestGetSizeTags:
    def setup_method(self):
        self.agent = TagAgent()

    def test_small(self):
        assert "small" in self.agent._get_size_tags("4x6")

    def test_medium(self):
        assert "medium" in self.agent._get_size_tags("8x10")

    def test_large(self):
        assert "large" in self.agent._get_size_tags("16x20")

    def test_unknown(self):
        assert self.agent._get_size_tags("custom") == []

    def test_small_keyword(self):
        assert "small" in self.agent._get_size_tags("small print")


class TestGetColorTags:
    def setup_method(self):
        self.agent = TagAgent()

    def test_monochrome(self):
        assert "monochrome" in self.agent._get_color_tags(["black"])

    def test_multi_color(self):
        tags = self.agent._get_color_tags(["red", "blue", "green", "yellow"])
        assert "multi_color" in tags

    def test_high_contrast(self):
        tags = self.agent._get_color_tags(["black", "red"])
        assert "high_contrast" in tags

    def test_earth_tones(self):
        tags = self.agent._get_color_tags(["brown", "green"])
        assert "earth_tones" in tags


class TestGetToolTags:
    def setup_method(self):
        self.agent = TagAgent()

    def test_pfeil(self):
        assert "pfeil_tools" in self.agent._get_tool_tags("pfeil v-gouge")

    def test_flexcut(self):
        assert "flexcut_tools" in self.agent._get_tool_tags("flexcut knife")

    def test_speedball(self):
        assert "speedball_tools" in self.agent._get_tool_tags("speedball gouge")

    def test_no_match(self):
        assert self.agent._get_tool_tags("generic tool") == []


class TestGenerateTags:
    def setup_method(self):
        self.agent = TagAgent()

    def test_full_metadata(self):
        metadata = {
            "title": "Abstract Landscape",
            "medium": "Linocut",
            "size": "8x10",
            "colors_used": ["black", "white"],
            "carving_tools": "pfeil v-gouge",
            "notes": "reduction print",
        }
        tags = self.agent._generate_tags(metadata)
        assert isinstance(tags, list)
        assert len(tags) > 0

    def test_minimal_metadata(self):
        metadata = {"title": "Test"}
        tags = self.agent._generate_tags(metadata)
        assert isinstance(tags, list)


class TestProcess:
    def setup_method(self):
        self.agent = TagAgent()

    def test_adds_tags(self):
        metadata = {
            "title": "Nature Scene",
            "colors_used": ["black", "white"],
        }
        result = self.agent.process(metadata, "/tmp/fake")
        assert "tags" in result

    def test_does_not_mutate_original(self):
        metadata = {"title": "Test"}
        self.agent.process(metadata, "/tmp/fake")
        assert "tags" not in metadata
