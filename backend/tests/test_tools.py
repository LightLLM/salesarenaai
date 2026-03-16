"""Unit tests for tools.py"""
import pytest
from app.tools import detect_objection, score_sales_skill


class TestDetectObjection:
    def test_returns_dict(self):
        result = detect_objection("budget", "We offer flexible pricing tiers.")
        assert isinstance(result, dict)

    def test_status_key_present(self):
        result = detect_objection("budget", "We offer flexible pricing tiers.")
        assert "status" in result

    def test_status_contains_objection_type(self):
        result = detect_objection("competitor", "Our platform outperforms competitors by 3x.")
        assert "competitor" in result["status"]

    def test_all_objection_types(self):
        for objection_type in ["budget", "competitor", "timing", "roi"]:
            result = detect_objection(objection_type, "Some user statement")
            assert objection_type in result["status"]

    def test_empty_user_statement(self):
        result = detect_objection("timing", "")
        assert "status" in result

    def test_status_message_format(self):
        result = detect_objection("budget", "We save you 30% annually.")
        assert "logged" in result["status"].lower() or "budget" in result["status"]


class TestScoreSalesSkill:
    def test_returns_dict(self):
        result = score_sales_skill(
            confidence=8,
            objection_handling=7,
            clarity=9,
            value_framing=8,
            closing=6,
            feedback="Good job on clarity. Work on closing techniques."
        )
        assert isinstance(result, dict)

    def test_status_key_present(self):
        result = score_sales_skill(
            confidence=5,
            objection_handling=5,
            clarity=5,
            value_framing=5,
            closing=5,
            feedback="Average performance overall."
        )
        assert "status" in result

    def test_status_indicates_scorecard_generated(self):
        result = score_sales_skill(
            confidence=10,
            objection_handling=10,
            clarity=10,
            value_framing=10,
            closing=10,
            feedback="Excellent pitch."
        )
        assert "scorecard" in result["status"].lower() or "generated" in result["status"].lower()

    def test_minimum_scores(self):
        result = score_sales_skill(
            confidence=1,
            objection_handling=1,
            clarity=1,
            value_framing=1,
            closing=1,
            feedback="Needs significant improvement."
        )
        assert "status" in result

    def test_maximum_scores(self):
        result = score_sales_skill(
            confidence=10,
            objection_handling=10,
            clarity=10,
            value_framing=10,
            closing=10,
            feedback="Perfect pitch."
        )
        assert "status" in result

    def test_long_feedback_string(self):
        long_feedback = "x" * 1000
        result = score_sales_skill(
            confidence=7,
            objection_handling=7,
            clarity=7,
            value_framing=7,
            closing=7,
            feedback=long_feedback
        )
        assert "status" in result
