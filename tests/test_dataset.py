import pytest
from pathlib import Path
import json

from src.friction_reasoning.dataset.generate_dataset import generate_question
from src.friction_reasoning.llm.client import LLMClient

@pytest.fixture
def llm_client():
    """Fixture for the LLMClient."""
    return LLMClient(model="mock/mock-model")

@pytest.mark.asyncio
async def test_generate_question_not_empty(llm_client):
    """Test that a generated question is not empty."""
    # Mock the async complete method
    async def mock_complete(prompt):
        return "This is a mock question?"
    
    llm_client.complete = mock_complete
    
    question = await generate_question(llm_client)
    assert isinstance(question, str)
    assert len(question) > 0

def test_dataset_file_exists_and_is_valid():
    """Test that the sample dataset file exists and is a valid JSONL."""
    dataset_path = Path("src/friction_reasoning/dataset/disagreement_dataset.jsonl")
    assert dataset_path.is_file(), "Dataset file does not exist."

    with open(dataset_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                # Check for required keys
                assert "id" in data
                assert "user_input" in data
                assert "agents" in data
                assert "metadata" in data
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON in dataset file: {line}")
            except AssertionError as e:
                pytest.fail(f"Missing key in dataset entry: {e}")
