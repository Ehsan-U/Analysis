from langchain.prompts import ChatPromptTemplate
# Chain 1
first_prompt = ChatPromptTemplate.from_template(
"""
Companies usually give their employees their own company email when they join. These emails are usually built using the names of the employees. For example, if the employee name is oskar martinez, his email could of the form: oskar@company_domain.com, oskarmartinez@company_domain.com, o.martinez@company_domain.com, m.oskar@company_domain.com, moskar@company_domain.com, and omartinez@company_domain.com
Now you are tasked to find such emails from a given list of emails. The email addresses are delimited by triple backticks. You have to identify all the email addresses have the names of the employee in them in some form. 
The names in the emails can be from any language.
Any generic email address that have the name of a product, job title, country or department etc such as sales@sama.bs.it, xxx@sama.bs.it, mexico@marcegaglia.com, financial@ibm.co.uk, director@ibm.co.uk are not required since we only trying to analyze emails with employee's personal name in it. Only output the email addresses that you believe to have the names of company employees in them. 
Just identify the email addresses and do not output anything else. If you do not find any email addresses in the set of emails addresses that have the names of employees in them below then just output NONE

Input emails: ``` {docs} ```

Make sure to include any email you find from the Input emails above that has the first name, last name, or their name initials in the email addresses in your answer
Helpful Answer in text format:
"""
)

# chain 2
second_prompt = ChatPromptTemplate.from_template(
"""
Input Emails: 
###
{emails}
###

Companies usually have a pattern with which they make the emails of their employees when they join. It is related to the names of the employees.
Given a list of employee emails delimited by triple hashtags, analyze the pattern individually and then in conclusion, find the most commonly found pattern among the emails.

You have two headings to output:
1. Individual email analysis one by one
-Email address:
-Email structure:
2. Conclusion
-Single most common pattern found:

If you cannot identify any pattern in the given emails, then just output NONE in that section
Helpful Answer in Text format:
"""
)

from langchain.prompts import PromptTemplate

third_prompt_template = """
You are given an identified email structure (delimited by triple backticks) for a particular email list (delimited by triple hashtags) below. 
You are tasked to find if the identified pattern matches most of the email list or not.
First give a detailed analysis if it is correct or not.
If the identified email structure is correct, then output it. Otherwise, output the correct structure.

Email list:``` {emails} ```
identified email Structure: ### {structure} ###

You have to output two headings
1. Detailed Analysis with logical arguments if the identified email structure is correct or not: 
2. Final email structure:
"""

input_vars = ["structure", "emails"]
third_prompt = PromptTemplate(input_variables=input_vars, template=third_prompt_template)

