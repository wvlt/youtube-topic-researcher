"""
Setup script for YouTube Content Researcher Agent
"""

from setuptools import setup, find_packages

setup(
    name="youtube-topic-researcher",
    version="1.0.0",
    description="AI-powered content research agent for YouTube creators",
    author="Amir Charkhi",
    packages=find_packages(),
    install_requires=[
        'google-api-python-client>=2.103.0',
        'google-auth-oauthlib>=1.1.0',
        'google-auth-httplib2>=0.1.1',
        'openai>=1.40.0',
        'anthropic>=0.34.0',
        'pyyaml>=6.0.1',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'tinydb>=4.8.0',
        'rich>=13.7.0',
        'click>=8.1.7',
        'pydantic>=2.5.0',
        'tenacity>=8.2.3',
        'pandas>=2.1.0',
        'numpy>=1.24.0',
        'lxml>=4.9.0',
        'pytrends>=4.9.0',
        'flask>=3.0.0',
        'flask-cors>=4.0.0',
    ],
    entry_points={
        'console_scripts': [
            'researcher=src.main:main',
        ],
    },
    python_requires='>=3.9',
)

