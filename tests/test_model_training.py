import pytest
from unittest.mock import MagicMock
import yaml
from pathlib import Path

from src.friction_reasoning.model_training import test_model

# Create a dummy config.yaml for testing
DUMMY_CONFIG = {
    "model_config": {
        "base_model": "mock/model",
        "model_max_length": 512,
    },
    "output_config": {
        "output_dir": "/tmp/mock_output",
    }
}

@pytest.fixture
def mock_config_file(tmp_path):
    """Create a temporary config file for tests."""
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(DUMMY_CONFIG, f)
    return config_path

def test_load_config(mock_config_file):
    """Test that the configuration loads correctly."""
    config = test_model.load_config(config_path=mock_config_file)
    assert config["model_config"]["base_model"] == "mock/model"

def test_generate_response_parsing():
    """Test the parsing of the model's raw output string."""
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()

    # Simulate raw output from the tokenizer
    raw_output = "<|im_start|>system\nHi<|im_end|>\n<|im_start|>user\nQ<|im_end|>\n<|im_start|>assistant\nThis is the answer.<|im_end|>"
    mock_tokenizer.decode.return_value = raw_output
    
    # We are testing the parsing logic inside generate_response, so we don't
    # need a real model call. We can mock the inputs.
    response = test_model.generate_response(mock_model, mock_tokenizer, "Dummy Prompt")
    
    assert response == "This is the answer."

def test_generate_response_parsing_error():
    """Test that parsing handles an unexpected format gracefully."""
    mock_model = MagicMock()
    mock_tokenizer = MagicMock()

    # Simulate a malformed output
    raw_output = "This is just a raw string without the expected format."
    mock_tokenizer.decode.return_value = raw_output
    
    response = test_model.generate_response(mock_model, mock_tokenizer, "Dummy Prompt")
    
    assert "Error: Could not parse response" in response
