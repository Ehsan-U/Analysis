from langchain.prompts import PromptTemplate
# Chain 1

recognition_template = """
For the company called: {company}
Given the set of company domains delimited by triple backticks, pick one domain that belong to the company called {company}.
If you believe that no given domain belongs to {company} then just output NONE
 
domains:
```
{text}
```

{company} domain:
"""

input_vars = ["company", "text"]
recognition_prompt = PromptTemplate(input_variables=input_vars, template=recognition_template)


