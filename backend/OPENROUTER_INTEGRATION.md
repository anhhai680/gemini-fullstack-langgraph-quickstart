# OpenRouter Integration Guide

This document explains how to use the OpenRouter integration to access free models like `gpt-oss-20b` in your LangGraph agent.

## Overview

The OpenRouter integration allows you to use free, high-quality language models from various providers through a single API. This significantly reduces costs while maintaining the quality of your research agent.

## Available Free Models

The following free models are available through OpenRouter:

- **gpt-oss-20b** (OpenAI) - 20B parameter model, excellent for reasoning and analysis
- **llama-3.1-8b-instruct** (Meta) - 8B parameter model, good for general tasks
- **gemma-2-9b-it** (Google) - 9B parameter model, efficient and reliable

## Setup

### 1. Get OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Environment Variables

Copy `env.template` to `.env` and fill in your API keys:

```bash
cp env.template .env
```

Edit `.env` with your actual API keys:

```bash
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-your_actual_key_here

# Google Gemini Configuration (fallback)
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

## Usage

### Automatic Model Selection

The system automatically detects when you're using an OpenRouter model and routes requests accordingly:

- **OpenRouter models**: Used for query generation, reflection, and answer generation
- **Gemini models**: Used as fallback and for Google Search API integration

### Model Configuration

You can configure different models for different tasks:

```bash
# Use gpt-oss-20b for all tasks
QUERY_GENERATOR_MODEL=gpt-oss-20b
REFLECTION_MODEL=gpt-oss-20b
ANSWER_MODEL=gpt-oss-20b

# Or mix and match
QUERY_GENERATOR_MODEL=gpt-oss-20b
REFLECTION_MODEL=llama-3.1-8b-instruct
ANSWER_MODEL=gemma-2-9b-it
```

### Fallback Behavior

If OpenRouter is unavailable or if you need Google Search API integration, the system automatically falls back to Gemini models.

## Architecture

### LLM Factory

The `LLMFactory` class handles model creation and routing:

- Automatically detects OpenRouter vs Gemini models
- Creates appropriate LLM instances
- Handles API configuration and headers

### Configuration

The `Configuration` class supports both OpenRouter and Gemini models:

- Environment variable overrides
- Runtime configuration updates
- Fallback model support

## Benefits

1. **Cost Savings**: Free access to high-quality models
2. **Model Diversity**: Access to models from multiple providers
3. **Automatic Fallback**: Seamless switching between providers
4. **Easy Configuration**: Simple environment variable setup
5. **Maintained Functionality**: All existing LangGraph features preserved

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `OPENROUTER_API_KEY` is set correctly
2. **Model Not Found**: Check that the model name is in the `FREE_MODELS` list
3. **Rate Limiting**: OpenRouter has rate limits on free tier

### Debug Mode

To debug model selection, check the logs for which LLM factory is being used.

## Performance Considerations

- **gpt-oss-20b**: Best performance, highest quality
- **llama-3.1-8b-instruct**: Good balance of speed and quality
- **gemma-2-9b-it**: Fastest, good for simple tasks

## Support

For OpenRouter-specific issues, visit [OpenRouter Support](https://openrouter.ai/docs).
For integration issues, check the LangGraph documentation.

