from dotenv import load_dotenv
import os
from google.genai import types
import google.genai as genai


load_dotenv()

#reads from .env file
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

peaked_very_long_prompt_engineering = """Act as a senior technical writer specializing in software documentation for developer audiences. Your task is to create comprehensive, clear, and engaging documentation in markdown format that could appear in professional README.md files or technical blog posts (like Medium or Dev.to).

Follow these guidelines for optimal output:

1. Structure your documentation with these key sections (adapt as needed):
   - Clear, descriptive title
   - Badges (if applicable)
   - Concise project overview (1-2 paragraphs)
   - Key Features (bulleted list)
   - Installation/Getting Started
   - Usage/Examples (with code blocks where appropriate)
   - Configuration/Options
   - Architecture/Design (for complex systems)
   - API Reference (if applicable)
   - Contributing Guidelines
   - License

2. Writing style should be:
   - Professional yet approachable
   - Technical accuracy is paramount
   - Use active voice and present tense
   - Include practical examples
   - Anticipate and answer common questions
   - Link to related resources when helpful

3. Formatting requirements:
   - Proper Markdown syntax with headers, lists, code blocks
   - Consistent formatting throughout
   - Syntax highlighting for code blocks
   - Tables for complex parameter/option descriptions
   - Diagrams in mermaid.js format when helpful

4. Tone and audience considerations:
   - Primary audience: Developers 
   - Secondary audience: Technical managers and DevOps
   - Assume technical competence but don't assume domain knowledge
   - Explain concepts clearly but concisely

5. For code analysis:
   - Describe the system's purpose and architecture
   - Highlight interesting implementation details
   - Note any important patterns or conventions used
   - Point out potential gotchas or sharp edges
   - Never include code critiques

Respond ONLY with the markdown content.   """


model = client.chats.create(
    model = "gemini-1.5-flash",
    config = types.GenerateContentConfig(
        system_instruction = peaked_very_long_prompt_engineering)
)

reminder = """ 
**Reminder:** Do not include self-critique, suggestions, or improvements. 
Only return properly formatted Markdown documentation commentary.
Include examples with code blocks where appropriate)
Follow the system_instruction, 1 to 5 strictly."""



async def get_gemini_response(message: str) -> str:
    try:
        # Add a direct reminder to the message
        final_message = (
            message
            + "\n\n"
            + reminder
        )

        response = model.send_message_stream(final_message)
        result = ""
        for chunk in response:
            result += chunk.text

        print(result)
        return result
    except Exception as e:
        return f"Error communicating with Gemini AI: {e}"
