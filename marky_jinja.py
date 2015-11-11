#name: marky_jinja
#author: Smirnov Kirill
#revision: 1.0
#revision date: 09.11.2015
#description: this app uses advantages of markdown and jinja templating to make static site. it renders markdown file to temporary_html and after it renders temporary_html to ready_html with header, footer and css (theme) via jinja. ready static html can be used as usual static site (for example, githubpages) 


#!/usr/bin/python3
import markdown
from jinja2 import Environment, FileSystemLoader
from subprocess import call


#global variables
source_folder = 'source' #where lies source files
main_template = 'header-footer.html' #this stuff + css = theme
content_list = ['index']#,'faq','uslugi'] #site pages names
params_list = ['.md', '_temp.html', '.html'] #convention for this app
extensions = ['markdown.extensions.nl2br', 'markdown.extensions.extra']
yes_answers = ['y', 'Y', 'yes', 'Yes'] #how user can confirm git renew

def file_name (name):
    file_name = []
    for param in params_list:
        if param == '.html':
            string_name = name + param
        else:
            string_name = source_folder + '/' + name + param
        file_name.append(string_name)
    return file_name

def make_md (content_md, temp_html):
    markdown.markdownFromFile (content_md, temp_html, extensions)

def make_jinja (temp_html, ready_html):
    env = Environment(loader=FileSystemLoader(source_folder))
    template = env.get_template(main_template)
    content_object = open(temp_html)
    output = template.render(foo = content_object.read())
    with open(ready_html, 'w') as f:
        f.write(output)

def make_site ():
    for name in content_list:
        variables = file_name (name)
        make_md (variables[0], variables[1])
        make_jinja (variables[1], variables[2])

def git_renew ():
    print ("html_pages of your site, are ready. should i add-commit-push it to git?")
    answer = input ("(y/N)>")
    if answer in yes_answers:
        #actually, its completely wrong, i should ask comment to input
        call (["git add ."])
        call (["git commit -m 'some comment'"])
        call (["git push origin master"])
    else:
        print ("ok, sir, bye!")


make_site ()
git_renew ()