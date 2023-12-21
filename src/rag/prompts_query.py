from langchain.prompts import PromptTemplate

query_template = """
If you do not know the answer then disregard everything you read below and just output: <no answer>.

For the company called {company_name}, answer my query below.
Note: If the query is asking for the company's domain, it means it's asking for the company's email domain.
for example, in the email sawaiz@ibm.co.uk, the domain would be ibm.co.uk.
Give me a detailed answer for the query, output everything that you know. Do not skip anything on the topic
In your output, make sure you are writing each piece of information line by line like a list of facts.
<QUERY>: {query}
"""
input_vars = ["company_name", "query"]
query_prompt = PromptTemplate(input_variables=input_vars, template=query_template)

keyword_refiner_template = """
For the company called {company_name}, I have been given a certain keyword pharse: {keyword}
Your job is to create a simple sentence query for this keyword that shapes the keyword into a general question about the company.
For example, if you get the keyword "has electric furnace", you query would be: "Does the company has electric furnace?"
For example, if you get the keyword "production sites", you query would be: "Tell me about the company's production sites?"

<QUERY>: 
"""
input_vars = ["company_name", "keyword"]
keyword_prompt = PromptTemplate(input_variables=input_vars, template=keyword_refiner_template)