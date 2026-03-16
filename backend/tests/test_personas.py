"""Unit tests for personas.py"""
import pytest
from app.personas import PERSONAS

REQUIRED_PERSONA_KEYS = {"name", "prompt"}
EXPECTED_PERSONA_IDS = {"skeptic", "budget_guardian", "procurement"}


class TestPersonasStructure:
    def test_personas_is_dict(self):
        assert isinstance(PERSONAS, dict)

    def test_all_expected_personas_exist(self):
        for persona_id in EXPECTED_PERSONA_IDS:
            assert persona_id in PERSONAS, f"Persona '{persona_id}' missing from PERSONAS"

    def test_no_extra_personas_without_review(self):
        """Ensure we're aware of all defined personas."""
        assert set(PERSONAS.keys()) == EXPECTED_PERSONA_IDS

    def test_each_persona_has_required_keys(self):
        for persona_id, persona in PERSONAS.items():
            for key in REQUIRED_PERSONA_KEYS:
                assert key in persona, f"Persona '{persona_id}' missing key '{key}'"

    def test_name_is_non_empty_string(self):
        for persona_id, persona in PERSONAS.items():
            assert isinstance(persona["name"], str), f"'{persona_id}' name is not a string"
            assert len(persona["name"].strip()) > 0, f"'{persona_id}' name is empty"

    def test_prompt_is_non_empty_string(self):
        for persona_id, persona in PERSONAS.items():
            assert isinstance(persona["prompt"], str), f"'{persona_id}' prompt is not a string"
            assert len(persona["prompt"].strip()) > 0, f"'{persona_id}' prompt is empty"

    def test_prompt_has_minimum_length(self):
        """Prompts should be substantive enough to drive behavior."""
        for persona_id, persona in PERSONAS.items():
            assert len(persona["prompt"]) >= 50, f"'{persona_id}' prompt is too short"


class TestSkepticPersona:
    def setup_method(self):
        self.persona = PERSONAS["skeptic"]

    def test_name_contains_skeptic(self):
        assert "skeptic" in self.persona["name"].lower() or "Skeptic" in self.persona["name"]

    def test_prompt_mentions_cto_or_technical(self):
        prompt_lower = self.persona["prompt"].lower()
        assert "cto" in prompt_lower or "technical" in prompt_lower or "proof" in prompt_lower

    def test_prompt_sets_adversarial_behavior(self):
        prompt_lower = self.persona["prompt"].lower()
        assert any(word in prompt_lower for word in ["flaw", "skeptic", "demand", "interrupt"])


class TestBudgetGuardianPersona:
    def setup_method(self):
        self.persona = PERSONAS["budget_guardian"]

    def test_name_contains_budget(self):
        assert "budget" in self.persona["name"].lower() or "Budget" in self.persona["name"]

    def test_prompt_mentions_roi_or_cost(self):
        prompt_lower = self.persona["prompt"].lower()
        assert "roi" in prompt_lower or "cost" in prompt_lower or "cfo" in prompt_lower

    def test_prompt_mentions_competitor_angle(self):
        prompt_lower = self.persona["prompt"].lower()
        assert "free" in prompt_lower or "good enough" in prompt_lower or "already have" in prompt_lower


class TestProcurementPersona:
    def setup_method(self):
        self.persona = PERSONAS["procurement"]

    def test_name_contains_procurement(self):
        assert "procurement" in self.persona["name"].lower() or "Procurement" in self.persona["name"]

    def test_prompt_mentions_price_or_cost(self):
        prompt_lower = self.persona["prompt"].lower()
        assert "price" in prompt_lower or "pricing" in prompt_lower or "expensive" in prompt_lower

    def test_prompt_sets_impatient_behavior(self):
        prompt_lower = self.persona["prompt"].lower()
        assert "impatient" in prompt_lower or "hurry" in prompt_lower or "interrupt" in prompt_lower
