#name: marky_jinja
#author: Smirnov Kirill
#revision: 1.3
#revision date: 22.11.2015
#description: this app uses advantages of markdown and jinja templating to make static site. it renders markdown
#file to temporary_html and after it renders temporary_html to ready_html with header, footer and css (theme)
#via jinja. ready html to be used as usual static site (i.e. githubpages)


#!/usr/bin/python3
import markdown
from jinja2 import Environment, FileSystemLoader
from subprocess import call


#edit this variables for your project
site_folder = '/home/path_to_your_project' #where your site lies
source_folder = 'source' #where source files lies
full_source_folder = site_folder + '/' + source_folder
main_template = 'header-footer.html' #this stuff + css = theme
params_list = ['.md', '_temp.html', '.html'] #convention for this app
extensions = ['markdown.extensions.nl2br', 'markdown.extensions.extra']


def make_content_list ():
    call ('ls ' + full_source_folder + ' > content_list.txt', shell =  True)
    with open ('content_list.txt') as f:
        content_list_raw = f.readlines()
    call ('rm content_list.txt', shell =  True)
    content_list = []
    for content in content_list_raw:
        if '.md' in content:
            content_list.append (content.split('.')[0])
    return content_list

def make_file_name (name):
    file_name = []
    for param in params_list:
        if param == '.html':
            string_name = site_folder + '/' + name + param
        else:
            string_name = full_source_folder + '/' + name + param
        file_name.append (string_name)
    return file_name

def make_md (content_md, temp_html):
    markdown.markdownFromFile (content_md, temp_html, extensions)

def make_jinja (temp_html, ready_html):
    env = Environment (loader = FileSystemLoader(full_source_folder))
    template = env.get_template (main_template)
    content_object = open (temp_html)
    output = template.render (foo = content_object.read())
    with open (ready_html, 'w') as f:
        f.write (output)

def make_site ():
    content_list = make_content_list ()
    print ("script made:")
    for name in content_list:
        file_name = make_file_name (name)
        make_md (file_name[0], file_name[1])
        make_jinja (file_name[1], file_name[2])
        call ('rm ' + file_name[1], shell = True)
        print (name)
    print ("html pages total = %d" % len (content_list))


make_site ()