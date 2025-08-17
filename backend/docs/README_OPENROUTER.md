# OpenRouter Integration for LangGraph Agent

This document provides a complete guide to using OpenRouter with your LangGraph research agent to access free, high-quality language models.

## 🚀 Quick Start

### 1. Get OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Set Environment Variables
```bash
# Copy the template
cp env.template .env

# Edit .env with your API keys
OPENROUTER_API_KEY=sk-or-v1-your_actual_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Model Configuration
QUERY_GENERATOR_MODEL=gpt-oss-20b
REFLECTION_MODEL=gpt-oss-20b
ANSWER_MODEL=gpt-oss-20b
USE_OPENROUTER=true
```

### 3. Install Dependencies
```bash
pip install -e .
```

### 4. Test Integration
```bash
python3 test_openrouter.py
```

## 🆓 Available Free Models

| Model | Provider | Parameters | Best For | Context Length |
|-------|----------|------------|----------|----------------|
| `gpt-oss-20b` | OpenAI | 20B | Reasoning, Analysis | 8,192 |
| `llama-3.1-8b-instruct` | Meta | 8B | General Tasks | 8,192 |
| `gemma-2-9b-it` | Google | 9B | Fast, Simple Tasks | 8,192 |

## 🔧 Configuration Options

### All OpenRouter Models (Recommended for Free Tier)
```python
config = Configuration(
    query_generator_model="gpt-oss-20b",
    reflection_model="gpt-oss-20b",
    answer_model="gpt-oss-20b",
    use_openrouter=True
)
```

### Mixed Models (Cost Optimization)
```python
config = Configuration(
    query_generator_model="gpt-oss-20b",      # OpenRouter (free)
    reflection_model="llama-3.1-8b-instruct", # OpenRouter (free)
    answer_model="gemini-2.5-pro",            # Gemini (paid)
    use_openrouter=True
)
```

### Performance Optimized
```python
config = Configuration(
    query_generator_model="gemma-2-9b-it",    # Fast
    reflection_model="gpt-oss-20b",           # High Quality
    answer_model="gpt-oss-20b",               # High Quality
    use_openrouter=True
)
```

## 🏗️ Architecture

### LLM Factory
The `LLMFactory` class automatically handles:
- Model detection (OpenRouter vs Gemini)
- API configuration
- Fallback behavior
- Error handling

### Automatic Routing
- **OpenRouter models**: Used for query generation, reflection, and answer generation
- **Gemini models**: Used as fallback and for Google Search API integration

### Configuration
The `Configuration` class supports:
- Environment variable overrides
- Runtime configuration updates
- Model validation
- Provider selection

## 📊 Benefits

1. **Cost Savings**: Free access to high-quality models
2. **Model Diversity**: Access to models from multiple providers
3. **Automatic Fallback**: Seamless switching between providers
4. **Easy Configuration**: Simple environment variable setup
5. **Maintained Functionality**: All existing LangGraph features preserved

## 🔍 Usage Examples

### Basic Usage
```python
from agent.configuration import Configuration
from agent.llm_factory import LLMFactory

# Create configuration
config = Configuration()

# Create LLM factory
factory = LLMFactory(config)

# Create LLMs for different tasks
query_llm = factory.create_llm("query_generator", temperature=0.7)
reflection_llm = factory.create_llm("reflection", temperature=0.7)
answer_llm = factory.create_llm("answer", temperature=0.7)
```

### Custom Configuration
```python
# Override default models
config = Configuration(
    query_generator_model="llama-3.1-8b-instruct",
    reflection_model="gpt-oss-20b",
    answer_model="gemma-2-9b-it"
)

# Use in your agent
factory = LLMFactory(config)
```

## 🧪 Testing

### Run Test Suite
```bash
python3 test_openrouter.py
```

### Run Examples
```bash
python3 config_examples.py
python3 examples/openrouter_example.py
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ❌ OPENROUTER_API_KEY environment variable is required
   ```
   **Solution**: Set `OPENROUTER_API_KEY` in your `.env` file

2. **Model Not Found**
   ```
   ❌ Model llama-3.1-8b-instruct not found in free models
   ```
   **Solution**: Check the model name spelling in `FREE_MODELS`

3. **Rate Limiting**
   ```
   ❌ Rate limit exceeded
   ```
   **Solution**: OpenRouter has rate limits on free tier

### Debug Mode
Check the logs for which LLM factory is being used:
```python
factory = LLMFactory(config)
print(f"Is OpenRouter model: {factory._is_openrouter_model('gpt-oss-20b')}")
```

## 📈 Performance Considerations

| Model | Speed | Quality | Best Use Case |
|-------|-------|---------|---------------|
| `gpt-oss-20b` | Medium | High | Complex reasoning, analysis |
| `llama-3.1-8b-instruct` | Fast | Good | General tasks, simple reasoning |
| `gemma-2-9b-it` | Very Fast | Good | Simple tasks, quick responses |

## 🔒 Security

- API keys are stored in environment variables
- No hardcoded credentials in the code
- Secure API communication via HTTPS
- Rate limiting protection

## 📚 Additional Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 🤝 Support

- **OpenRouter Issues**: [OpenRouter Support](https://openrouter.ai/docs)
- **Integration Issues**: Check the LangGraph documentation
- **Model Performance**: Test different models for your use case

## 📝 Changelog

### v1.0.0 - Initial Release
- OpenRouter integration with free models
- LLM factory for automatic routing
- Configuration management
- Fallback to Gemini models
- Comprehensive testing suite

---

**Happy coding with free AI models! 🎉**

