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
Helpful Answer:
"""
)

# chain 2
second_prompt = ChatPromptTemplate.from_template(
"""
Companies usually have a pattern with which they make the emails of their employees when they join. It is related to the names of the employees.
Given a list of employee emails delimited by triple hashtags, analyze the pattern individually and then give collective analysis, find the most commonly found pattern among the emails.

You have two headings to output:
1. Individual email analysis one by one:
-Email address:
-Email structure:
2. Comma seperated list of all email structures found: 
3. Most frequently repeated email structure:

Example 1:
```
Input Emails: ###
serge.santamaria@ascometal.com
louis-nicolas.hallez@ascometal.com
etienne.archaud@ascometal.com
contact.achats.fournisseurs@ascometal.com
alain.genta@ascometal.com
ascometal@ascometal.com
maxime.lazard@ascometal.com
contact@ascometal.com ###

Individual email analysis one by one:
-Email address: serge.santamaria@ascometal.com
-Email structure: [first name].[last name]@ascometal.com

-Email address: louis-nicolas.hallez@ascometal.com
-Email structure: [first name]-[middle name].[last name]@ascometal.com

-Email address: etienne.archaud@ascometal.com
-Email structure: [first name].[last name]@ascometal.com

-Email address: contact.achats.fournisseurs@ascometal.com
-Email structure: contact.department@ascometal.com

-Email address: alain.genta@ascometal.com
-Email structure: [first name].[last name]@ascometal.com

-Email address: ascometal@ascometal.com
-Email structure: generic@ascometal.com

-Email address: maxime.lazard@ascometal.com
-Email structure: [first name].[last name]@ascometal.com

-Email address: contact@ascometal.com
-Email structure: contact@ascometal.com

Comma seperated list of all email structures found in order: [[first name].[last name]@ascometal.com, [first name]-[middle name].[last name]@ascometal.com]
Most frequently repeated email structure:  [first name].[last name]@ascometal.com
```

Example 2:
```
Input Emails: 
###
m.oskar@company_domain.com
oskar@company_domain.com
oskarmartinez@company_domain.com
matthias.mack@company_domain.com
christoph.massner@company_domain.com
###

Individual email analysis one by one:
-Email address: m.oskar@company_domain.com
-Email structure: [first name initials (1)].[last name]@company_domain.com

-Email address: oskar@company_domain.com
-Email structure: [firstname]@company_domain.com

-Email address: oskarmartinez@company_domain.com
-Email structure: [firstname][lastname]@company_domain.com

-Email address: matthias.mack@company_domain.com
-Email structure: [firstname].[last name]@company_domain.com

-Email address: christoph.massner@company_domain.com
-Email structure: [firstname].[last name]@company_domain.com

Comma seperated list of all email structures found in order: [[first name initials (1)].[last name]@company_domain.com, [firstname]@company_domain.com, [firstname].[last name]@company_domain.com]
Most frequently repeated email structure: [firstname].[last name]@company_domain.com
```

Example 3:```
Input Emails: 
###
+astrid.winkler@t-online.de
+hubert.hentschel@t-online.de
+dr.merkelbach@t-online.de
+angelapatain@t-online.de
+bertl.heinz@t-online.de
+andreas-heindel@t-online.de
+domenicopecoraro@t-online.de
###

Individual email analysis one by one:
-Email address: +astrid.winkler@t-online.de
-Email structure: [first name].[last name]@t-online.de

-Email address: +hubert.hentschel@t-online.de
-Email structure: [first name].[last name]@t-online.de

-Email address: +dr.merkelbach@t-online.de
-Email structure: [title].[last name]@t-online.de

-Email address: +angelapatain@t-online.de
-Email structure: [first name][last name]@t-online.de

-Email address: +bertl.heinz@t-online.de
-Email structure: [first name].[last name]@t-online.de

-Email address: +andreas-heindel@t-online.de
-Email structure: [first name]-[last name]@t-online.de

-Email address: +domenicopecoraro@t-online.de
-Email structure: [firstname][lastname]@t-online.de

Comma seperated list of all email structures found: [[first name].[last name]@t-online.de,  [title].[last name]@t-online.de, [firstname][lastname]@t-online.de, [first name]-[last name]@t-online.de, [firstname][lastname]@t-online.de]
Most frequently repeated email structure:  [firstname].[last name]@company_domain.com
```

Example 4:```
Input Emails: 
###
matthias.mack@severstal.com
christoph.massner@severstal.com
ay.lohanov@severstal.com
aadmitrenko@severstal.com
ev.sizova@severstal.com
as.rogachev@severstal.com
rn.ursu@severstal.com
rr.kamalov@severstal.com
da.mokritcin@severstal.com
ola.borisova@severstal.com
dadontsov@severstal.com
ed.fedorovich@severstal.com
eakuznetsov@severstal.com
ia.sidun@severstal.com
oa.kvanina@severstal.com
iagruzdev@severstal.com
gl.sharmazanyan@severstal.com
ka.petrov@severstal.com
###

Individual email analysis one by one:
-Email address: matthias.mack@severstal.com
-Email structure: [first name].[last name]@severstal.com

-Email address: christoph.massner@severstal.com
-Email structure: [first name].[last name]@severstal.com

-Email address: ay.lohanov@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: aadmitrenko@severstal.com
-Email structure: [first name initial (1 initial)][last name]@severstal.com

-Email address: ev.sizova@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: as.rogachev@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: rn.ursu@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: rr.kamalov@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: da.mokritcin@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: ola.borisova@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: dadontsov@severstal.com
-Email structure: [first name initial (1 initial)][last name]@severstal.com

-Email address: ed.fedorovich@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: eakuznetsov@severstal.com
-Email structure: [first name initials (2 initials)][last name]@severstal.com

-Email address: ia.sidun@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: oa.kvanina@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: iagruzdev@severstal.com
-Email structure: [first name initials (2 initials)][last name]@severstal.com

-Email address: gl.sharmazanyan@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

-Email address: ka.petrov@severstal.com
-Email structure: [first name initials (2 initials)].[last name]@severstal.com

Comma seperated list of all email structures found: [[first name initials (2 initials)].[last name]@severstal.com, [first name].[last name]@severstal.com, [first name initial (1 initial)][last name]@severstal.com]
Most frequently repeated email structure: [first name initials (2 initials)].[last name]@severstal.com
```

Example 4:```
Input Emails: ###
kamynina_ei2@nlmk.com
rimskaya_aa@nlmk.com
zatsepina_ty@nlmk.com
kruglov_ds@nlmk.com
magomedova_vv@nlmk.com
dezhkova_ka@nlmk.com
melnikov_ai@nlmk.com
loskutov_va@nlmk.com
###

Individual email analysis one by one:
-Email address: kamynina_ei2@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)][number]@nlmk.com

-Email address: rimskaya_aa@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)]@nlmk.com

-Email address: zatsepina_ty@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)]@nlmk.com

-Email address: kruglov_ds@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)]@nlmk.com

-Email address: magomedova_vv@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)]@nlmk.com

-Email address: dezhkova_ka@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)]@nlmk.com

-Email address: melnikov_ai@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)]@nlmk.com

-Email address: loskutov_va@nlmk.com
-Email structure: [last name]_[first name initials (2 initials)]@nlmk.com

Comma seperated list of all email structures found: [last name]_[first name initials (2 initials)]@nlmk.com, [last name]_[first name initials (2 initials)][number]@nlmk.com
Most frequently repeated email structure: [last name]_[first name initials (2 initials)]@nlmk.com
```

Example 4:```
Input Emails: ###
karriere@salzgitter-ag.com
alsmannm@salzgitter-ag.com
###

Individual email analysis one by one:
-Email address: karriere@salzgitter-ag.com
-Email structure: NONE

-Email address: alsmannm@salzgitter-ag.com
-Email structure: [last name]@salzgitter-ag.com

Comma seperated list of all email structures found: [last name]@salzgitter-ag.com
Most frequently repeated email structure: [last name]@salzgitter-ag.com
```

Example 5:```
Input Emails: ###
bobansrsc@hbisserbia.rs
dlovre@hbisserbia.rs
vgergulov@hbisserbia.rs
vladimirnovakovic@hbisserbia.rs
mhinic@hbisserbia.rs
ijovicsrsc@hbisserbia.rs
lilijapopovic@hbisserbia.rs
danicaperovic@hbisserbia.rs
vselakovic@hbisserbia.rs
rmandicsrsc@hbisserbia.rs
dnikolic@hbisserbia.rs
draganajovic@hbisserbia.rs
g.milojevic@hbisserbia.rs
vpaunovic@hbisserbia.rs
danijelastefanovic@hbisserbia.rs
vladanandrejic@hbisserbia.rs
jovandjordjevic@hbisserbia.rs
###

Individual email analysis one by one:
-Email address: bobansrsc@hbisserbia.rs
-Email structure: NONE

-Email address: dlovre@hbisserbia.rs
-Email structure: [first name initials (1 initial)][last name]@hbisserbia.rs

-Email address: vgergulov@hbisserbia.rs
-Email structure: [first name initials (1 initial)][last name]@hbisserbia.rs

-Email address: vladimirnovakovic@hbisserbia.rs
-Email structure: [first name][last name]@hbisserbia.rs

-Email address: mhinic@hbisserbia.rs
-Email structure: [first name initials (1 initial)][last name]@hbisserbia.rs

-Email address: ijoicsrsc@hbisserbia.rs
-Email structure: NONE

-Email address: lilijapopovic@hbisserbia.rs
-Email structure: [first name][last name]@hbisserbia.rs

-Email address: danicaperovic@hbisserbia.rs
-Email structure: [first name][last name]@hbisserbia.rs

-Email address: vselakovic@hbisserbia.rs
-Email structure: [first name initials (1 initial)][last name]@hbisserbia.rs

-Email address: rmandicsrsc@hbisserbia.rs
-Email structure: NONE

-Email address: dnikolic@hbisserbia.rs
-Email structure: [first name initials (1 initial)][last name]@hbisserbia.rs

-Email address: draganajovic@hbisserbia.rs
-Email structure: [first name][last name]@hbisserbia.rs

-Email address: g.milojevic@hbisserbia.rs
-Email structure: [first name initials (1 initial)].[last name]@hbisserbia.rs

-Email address: vpaunovic@hbisserbia.rs
-Email structure: [first name initials (1 initial)][last name]@hbisserbia.rs

-Email address: danijelastefanovic@hbisserbia.rs
-Email structure: [first name][last name]@hbisserbia.rs

-Email address: vladanandrejic@hbisserbia.rs
-Email structure: [first name][last name]@hbisserbia.rs

-Email address: jovandjordjevic@hbisserbia.rs
-Email structure: [first name][last name]@hbisserbia.rs

Comma seperated list of all email structures found: [first name initials (1 initial)][last name]@hbisserbia.rs, [first name][last name]@hbisserbia.rs, [first name initials (1 initial)].[last name]@hbisserbia.rs
Most frequently repeated email structure: [first name initials (1 initial)][last name]@hbisserbia.rs
```
Example 6:```
Input Emails: ###
jpfisterer@ms-stahlhandel.at
nlobner@ms-stahlhandel.at
ascheuchenpflug@ms-stahlhandel.at
mbrungraber@ms-stahlhandel.at
dpfleger@ms-stahlhandel.at
hgahleitner@ms-stahlhandel.at
rbernhaider@ms-stahlhandel.at
###

Individual email analysis one by one:
-Email address: jpfisterer@ms-stahlhandel.at
-Email structure: [first name initials (1 initial)][last name]@ms-stahlhandel.att

-Email address: nlobner@ms-stahlhandel.at
-Email structure: [first name initials (1 initial)][last name]@ms-stahlhandel.at

-Email address: ascheuchenpflug@ms-stahlhandel.at
-Email structure: [first name initials (1 initial)][last name]@ms-stahlhandel.at

-Email address: mbrungraber@ms-stahlhandel.at
-Email structure: [first name initials (1 initial)][last name]@ms-stahlhandel.at

-Email address: dpfleger@ms-stahlhandel.at
-Email structure: [first name initials (2 initials)][last name]@ms-stahlhandel.at

-Email address: hgahleitner@ms-stahlhandel.at
-Email structure: [first name initials (1 initial)][last name]@ms-stahlhandel.at

-Email address: rbernhaider@ms-stahlhandel.at
-Email structure: [first name initials (1 initial)][last name]@ms-stahlhandel.at

Comma separated list of all email structures found: [first name initials (2 initials)][last name]@ms-stahlhandel.at, [first name initials (1 initial)][last name]@ms-stahlhandel.at
Most frequently repeated email structure: [first name initials (1 initial)][last name]@ms-stahlhandel.at
```

Input Emails: 
###
{emails}
###
If you cannot identify any pattern in the given emails, then just output NONE in that section.
Helpful Answer:
"""
)


from langchain.prompts import PromptTemplate

third_prompt_template = """
You are given an email structure analysis (delimited by triple backticks) for a particular email list (delimited by triple hashtags) below. \
    Your job is to pick 1 most commonly seen email structure. I don't want more than 1 email structure as output.

Email structure analysis: ```
{structure}
```

1 most frequently seen email structure in the email list in comma seperated list:
"""

input_vars = ["structure"]
third_prompt = PromptTemplate(input_variables=input_vars, template=third_prompt_template)