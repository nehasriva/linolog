"""Unit tests for ColorAgent."""

import os
import numpy as np
from unittest.mock import patch
from linolog.agents.color_agent import ColorAgent


class TestRgbToColorName:
    def setup_method(self):
        self.agent = ColorAgent()

    def test_red(self):
        assert self.agent._rgb_to_color_name(np.array([255, 50, 50])) == "red"

    def test_blue(self):
        assert self.agent._rgb_to_color_name(np.array([50, 50, 255])) == "blue"

    def test_green(self):
        assert self.agent._rgb_to_color_name(np.array([50, 255, 50])) == "green"

    def test_yellow(self):
        assert self.agent._rgb_to_color_name(np.array([255, 255, 50])) == "yellow"

    def test_purple(self):
        assert self.agent._rgb_to_color_name(np.array([255, 50, 255])) == "purple"

    def test_orange(self):
        assert self.agent._rgb_to_color_name(np.array([255, 150, 50])) == "orange"

    def test_brown(self):
        assert self.agent._rgb_to_color_name(np.array([150, 100, 50])) == "brown"

    def test_black(self):
        assert self.agent._rgb_to_color_name(np.array([10, 10, 10])) == "black"

    def test_white(self):
        assert self.agent._rgb_to_color_name(np.array([250, 250, 250])) == "white"

    def test_gray(self):
        assert self.agent._rgb_to_color_name(np.array([128, 128, 128])) == "gray"

    def test_ambiguous_returns_none(self):
        # A color that doesn't match any rule
        assert self.agent._rgb_to_color_name(np.array([100, 200, 150])) is None


class TestFindPrintImage:
    def setup_method(self):
        self.agent = ColorAgent()

    def test_prefers_final_image(self, tmp_path):
        (tmp_path / "random.jpg").touch()
        (tmp_path / "final_print.jpg").touch()
        result = self.agent._find_print_image(str(tmp_path))
        assert "final_print.jpg" in result

    def test_prefers_print_image(self, tmp_path):
        (tmp_path / "random.jpg").touch()
        (tmp_path / "my_print.png").touch()
        result = self.agent._find_print_image(str(tmp_path))
        assert "my_print.png" in result

    def test_falls_back_to_first_image(self, tmp_path):
        (tmp_path / "photo.png").touch()
        result = self.agent._find_print_image(str(tmp_path))
        assert "photo.png" in result

    def test_no_images_returns_none(self, tmp_path):
        (tmp_path / "notes.txt").touch()
        result = self.agent._find_print_image(str(tmp_path))
        assert result is None

    def test_empty_folder_returns_none(self, tmp_path):
        result = self.agent._find_print_image(str(tmp_path))
        assert result is None


class TestProcess:
    def setup_method(self):
        self.agent = ColorAgent()

    def test_no_image_returns_unchanged(self):
        metadata = {"title": "Test"}
        with patch.object(self.agent, "_find_print_image", return_value=None):
            result = self.agent.process(metadata, "/tmp/fake")
        assert result == metadata
        assert "colors_used" not in result

    def test_does_not_mutate_original(self):
        metadata = {"title": "Test"}
        with patch.object(self.agent, "_find_print_image", return_value=None):
            self.agent.process(metadata, "/tmp/fake")
        assert "colors_used" not in metadata
