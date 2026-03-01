"""Unit tests for LLMColorAgent."""

import numpy as np
from unittest.mock import patch, MagicMock
from linolog.agents.llm_color_agent import LLMColorAgent


class TestRgbToColorName:
    def setup_method(self):
        self.agent = LLMColorAgent(llm_client=None)

    def test_red(self):
        assert self.agent._rgb_to_color_name(np.array([255, 50, 50])) == "red"

    def test_blue(self):
        assert self.agent._rgb_to_color_name(np.array([50, 50, 255])) == "blue"

    def test_green(self):
        assert self.agent._rgb_to_color_name(np.array([50, 255, 50])) == "green"

    def test_black(self):
        assert self.agent._rgb_to_color_name(np.array([10, 10, 10])) == "black"

    def test_white(self):
        assert self.agent._rgb_to_color_name(np.array([250, 250, 250])) == "white"

    def test_ambiguous_returns_none(self):
        assert self.agent._rgb_to_color_name(np.array([100, 200, 150])) is None


class TestFindPrintImage:
    def setup_method(self):
        self.agent = LLMColorAgent(llm_client=None)

    def test_prefers_final(self, tmp_path):
        (tmp_path / "random.jpg").touch()
        (tmp_path / "final_print.jpg").touch()
        result = self.agent._find_print_image(str(tmp_path))
        assert "final_print.jpg" in result

    def test_falls_back_to_first(self, tmp_path):
        (tmp_path / "photo.png").touch()
        result = self.agent._find_print_image(str(tmp_path))
        assert "photo.png" in result

    def test_no_images_returns_none(self, tmp_path):
        (tmp_path / "notes.txt").touch()
        result = self.agent._find_print_image(str(tmp_path))
        assert result is None


class TestAnalyzeColorsWithLlm:
    def test_no_client_returns_none(self):
        agent = LLMColorAgent(llm_client=None)
        result = agent._analyze_colors_with_llm("/fake/image.jpg")
        assert result is None

    def test_success(self):
        mock_client = MagicMock()
        mock_client.analyze_image.return_value = "burnt sienna, forest green, ochre"
        agent = LLMColorAgent(llm_client=mock_client)

        with patch.object(agent, "_encode_image_to_base64", return_value="base64data"):
            result = agent._analyze_colors_with_llm("/fake/image.jpg")

        assert result == ["burnt sienna", "forest green", "ochre"]

    def test_llm_exception_returns_none(self):
        mock_client = MagicMock()
        mock_client.analyze_image.side_effect = Exception("API error")
        agent = LLMColorAgent(llm_client=mock_client)

        with patch.object(agent, "_encode_image_to_base64", return_value="base64data"):
            result = agent._analyze_colors_with_llm("/fake/image.jpg")

        assert result is None

    def test_limits_to_5_colors(self):
        mock_client = MagicMock()
        mock_client.analyze_image.return_value = "a, b, c, d, e, f, g"
        agent = LLMColorAgent(llm_client=mock_client)

        with patch.object(agent, "_encode_image_to_base64", return_value="base64data"):
            result = agent._analyze_colors_with_llm("/fake/image.jpg")

        assert len(result) == 5


class TestProcess:
    def test_no_image_returns_unchanged(self):
        agent = LLMColorAgent(llm_client=None)
        metadata = {"title": "Test"}
        with patch.object(agent, "_find_print_image", return_value=None):
            result = agent.process(metadata, "/tmp/fake")
        assert result == metadata
        assert "colors_used" not in result

    def test_llm_fallback_to_traditional(self):
        mock_client = MagicMock()
        agent = LLMColorAgent(llm_client=mock_client)

        with patch.object(
            agent, "_find_print_image", return_value="/fake/img.jpg"
        ), patch.object(
            agent, "_analyze_colors_with_llm", return_value=None
        ), patch.object(
            agent, "_analyze_colors_traditional", return_value=["red", "blue"]
        ):
            result = agent.process({"title": "Test"}, "/tmp/fake")

        assert result["colors_used"] == ["red", "blue"]

    def test_does_not_mutate_original(self):
        agent = LLMColorAgent(llm_client=None)
        metadata = {"title": "Test"}
        with patch.object(agent, "_find_print_image", return_value=None):
            agent.process(metadata, "/tmp/fake")
        assert "colors_used" not in metadata
