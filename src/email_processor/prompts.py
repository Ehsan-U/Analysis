from langchain.prompts import ChatPromptTemplate
# Chain 1
first_prompt = ChatPromptTemplate.from_template(
"""
Given the set of email addresses delimited by triple backticks identify all the email addresses that have the names of employees in it. Make sure to not included any generic email address for a product or department.
Example emails that I am looking for are like these which has some reference to the employee name: johnDoe@mckinsey.com, j.doe@ibm.com, john.d@tata.co.in 
Only output the email addresses that you think have the names of employees in them

```
{docs}
```
Just identify the email addreses and do not output anything else.
If you do not find any email addresses that have the names of employees then just output NONE
Helpful Answer in text format:
"""
)

# chain 2
second_prompt = ChatPromptTemplate.from_template(
"""
If you see NONE written in the text delimited by triple angle brackets then just output NONE and disregard any instruction you read below.

Given the following set of company email addresses delimited by triple angle brackets, identity the common pattern the company uses to build their employee 
emails. Since these are emails for the same company, they all have the same domain. I understand that so do not talk about it.
Only talk about the local-part which is the piece of email before the @ sign. I want to understand the pattern there.

Example results for reference:
Example Input emails: 
a.giovannelli@alfaacciai.it
u.dragani@alfaacciai.it
Results:
The common pattern for these company email addresses is:
`[first initial].[last name]@alfaacciai.it`
Example Input emails: 
NONE
Results:
NONE

Note: In these examples, it does not explain the alfacciai.it domain part, It only explains the local part.
Note: If it reads NONE then it just outputs NONE 
If you cannot identify any emails, then just output NONE

<<<
{emails}
<<<


Only use the emails in this message as reference. Do no include any email address you previously processed
Output NONE IF THERE ARE NO EMAILS PRESENT IN THE TEXT DELIMITED BY triple backticks
Helpful Answer:
"""
)

# chain 2
third_prompt = ChatPromptTemplate.from_template(
"""
If you see NONE written in the text delimited by triple backticks below then just output NONE and disregard any instruction you read below.

Using the patterns you have just identified, replace it with the following keys: 
[First Name]: for referring the first name
[Last Name]: for referring the last name
[First Name Intial]: for referring the intial of first name
[Last Name Initial]: for referring the initial of last name

I want to make sure the format is consistent for all the pattern email generated, so replace subtext with appropriate keys
Keep all punctutations or symbols used in the same place.

```
{patterns}
```

In the output, just write modified pattern email address. Do not write anything else
In the text delimited by triple backticks, if there is NONE written then your answer should be just NONE
I need the output in comma seperated list.

Helpful Answer:
"""
)

