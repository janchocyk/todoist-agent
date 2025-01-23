from setuptools import setup, find_packages

setup(
    name="todoist-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "python-dotenv>=1.0.0",
        "langgraph>=0.0.15",
        "anthropic>=0.7.7",
        "langchain-anthropic>=0.0.4",
        "todoist-api-python>=2.1.3",
        "pydantic>=2.5.2",
        "python-multipart>=0.0.6",
        "loguru>=0.7.2",
        "pydantic_settings"
    ],
    extras_require={
        "test": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.23.2",
            "httpx>=0.25.2",
            "pytest-cov>=4.1.0",
            "pytest-env>=1.1.1"
        ]
    }
)