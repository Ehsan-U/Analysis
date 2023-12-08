from langchain.prompts import PromptTemplate

from langchain.prompts import ChatPromptTemplate

map_template = """The following is a set of documents about the company called {company}: 
                {docs}
                Based on this list of docs about {company} given above, please extract the information mentioned in the headings below:
                Sections:
                1. Company Name
                2. Information about production sites for {company}
                3. Information about production process for {company}
                4. Information about production product range for {company}
                5. Information about company shared email addresses for {company}

                Note: when I say company email shared email address, it means the emails {company} uses for specific purposes is often referred to as a "generic" or "shared" email address. 
                If there is no information for a given section present in the given documents then just write NONE.
                For production sites, production process and product range headings, make sure not to skip any information and extract everything related to it. 
                Note: find maximum information related to the sections above. DO NOT MISS ANYTHING
                Helpful Answer:"""

input_vars = ["company", "docs"]
map_prompt = PromptTemplate(input_variables=input_vars, template=map_template)

reduce_template = """The following is set of summaries about the following company {company}:
                    {docs}
                    Take these and combine the information togather into following sections.                    
                    Sections:
                    1. Company Name: 
                    2. Information about production sites for {company}:
                    3. Information about production process for {company}:
                    4. Information about production product range for {company}:
                    5. Information about company email domains for {company}:

                    For the company email domains, only write the domains not the full addresses mentioned in the summaries above. For example, in info@alfaacciai.it, only extract the alfaacciai.it part.
                    For company email domain, only mention the possible domains for {company} that were identified in the summaries above.
                    Note: For heading about production sites, production process and product range, make sure not to skip any information and extract everything related to them.
                    If there is no information for a given section present in the given documents then just write NONE.
                    Helpful Answer:
                    """
input_vars = ["company", "docs"]
reduce_prompt = PromptTemplate(input_variables=input_vars, template=reduce_template)

query_template = """
            For the company called {company}, answer my query below.
            Note: If the query is asking for the company's domain, it means it's asking for the company's email domain.
            for example, in the email sawaiz@ibm.co.uk, the domain would be ibm.co.uk.
            Give me a detailed answer for my query.
            If you do not know the answer then just output single empty space. Just output empty space
            <QUERY>: {query}
        """

input_vars = ["company", "query"]
query_prompt = PromptTemplate(input_variables=input_vars, template=query_template)
