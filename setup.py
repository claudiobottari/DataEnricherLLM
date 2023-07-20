from setuptools import setup, find_packages

setup(
    name='DataEnricherLLM',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/claudiobottari/DataEnricherLLM',
    license='MIT',
    author='Claudio Bottari',
    author_email='bottari@gmail.com',
    description='A Python tool for enhancing LLMs like ChatGPT by enriching prompts with web-fetched information, improving response quality without affecting response time.',
    install_requires=[
        'openai==0.29.0',
        'python-dotenv>=0.19.1',
        'bs4==0.0.1',
        'requests>=2.26.0',
        'tiktoken>=0.4.0',
        'spacy>=3.6.0',
        'ggoogl esearc h-python>=',
        'pyperclip>=1.8.2',
        'cleantext>=1.1.4',
        'pandas'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
