from langchain.prompts import PromptTemplate

translation_template = """
For the company called: {company}
Given the set of pharses in different languages delimited by triple backticks, Make sure that all of them are converted to English.
I want the output as a comma seperated list for python.
Make sure that the number of translated pharses are the same as the original number of pharses. Hence, do not skip any pharse to translate. 
```
{text}
```
Translated titles: 
"""

input_vars = ["company", "text"]
translation_prompt = PromptTemplate(input_variables=input_vars, template=translation_template)


# translation_template = """
# For the company called: {company}
# Given the set of company job titles in different languages delimited by triple backticks, Make sure that all of them are converted to English.
# I want the output as a comma seperated list for python.
# Make sure that the number of translated titles are the same as the number of input job titles. That means if for any title you do not know the translation then just write that title back
# Otherwise, make you best guess.

# ```
# {text}
# ```

# Translated titles: 

# """