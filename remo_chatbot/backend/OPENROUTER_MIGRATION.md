# OpenRouter Migration Guide

## Changes Made

### 1. Removed SAMBANOVA Integration
- Removed all SAMBANOVA API configurations
- Removed SAMBANOVA_API_KEY from .env
- Removed SAMBANOVA_BASE_URL and SAMBANOVA_MODEL references

### 2. Implemented OpenRouter
- Added OPENROUTER_API_KEY to .env
- Configured OpenRouter base URL: `https://openrouter.ai/api/v1`
- Using `openai/gpt-4o-mini` for SQL generation (better accuracy)
- Using `openai/gpt-3.5-turbo` for result interpretation (faster)

### 3. Enhanced Chat Accuracy

#### SQL Generation Improvements:
- **Structured System Prompts**: Clear rules for SQL generation
- **Better Context**: Explicit database schema formatting
- **Syntax Validation**: Proper dialect-specific SQL generation
- **Token Limits**: Set max_tokens=500 for focused responses
- **Temperature=0.0**: Deterministic SQL generation

#### Result Interpretation Improvements:
- **Error Handling**: Better error messages for users
- **Empty Results**: Clear messaging when no data found
- **Data Formatting**: Smart truncation for large result sets
- **Natural Language**: Conversational responses
- **Context Preservation**: Includes original question and SQL in interpretation

#### API Enhancements:
- **Input Validation**: Check for empty questions
- **Response Metadata**: Added row_count to responses
- **Better Error Messages**: More descriptive error handling

## Configuration

Update your `.env` file:
```env
OPENROUTER_API_KEY="sk-or-v1-2550c6f45a184901090a14f16570942a759718d9450a2"
```

## Model Selection

You can change models in `llm_agent.py`:

```python
# For SQL generation (accuracy priority)
SQL_MODEL = "openai/gpt-4o-mini"  # or "anthropic/claude-3-sonnet"

# For interpretation (speed priority)
INTERPRET_MODEL = "openai/gpt-3.5-turbo"  # or "meta-llama/llama-3-8b-instruct"
```

## Benefits

1. **Better Accuracy**: GPT-4o-mini provides more reliable SQL generation
2. **Cost Effective**: OpenRouter offers competitive pricing
3. **Model Flexibility**: Easy to switch between different models
4. **Enhanced Prompts**: Structured prompts improve response quality
5. **Better UX**: Clear error messages and formatted responses

## Testing

Test the changes:
```bash
# Start the server
python main.py

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many records are in the users table?"}'
```
