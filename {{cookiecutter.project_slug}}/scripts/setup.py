from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import questionary
import subprocess
import re

# def get_prompt(question: dict):
#     if question['type'] == 'text':
#         return questionary.text(question['question'])
#     elif question['type'] == 'password':
#         return questionary.password(question['question'])
#     elif question['type'] == 'path':
#         return questionary.path(question['question'])
#     elif question['type'] == 'confirm':
#         return questionary.confirm(question['question'])
#     elif question['type'] == 'select':
#         return questionary.select(question['question'], choices=question['choices'])
#     elif question['type'] == 'rawselect':
#         return questionary.rawselect(question['question'], choices=question['choices'])
#     elif question['type'] == 'checkbox':
#         return questionary.checkbox(question['question'], choices=question['choices'])
#     elif question['type'] == 'autocomplete':
#         return questionary.autocomplete(question['question'], choices=question['choices'])
#     else:
#         raise ValueError(f'Unknown question type: {question["type"]}')



def is_integer(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def validate_url(url: dict):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None
   

def validate_package_version(item: dict):
    package_version = item.split('.')
    return all([is_integer(part) for part in package_version]) and len(package_version) == 3

def get_python_versions():
    
    MyOut = subprocess.Popen(['pyenv', 'install', '-l'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, universal_newlines=True)
    stdout,stderr = MyOut.communicate()
    return [version.strip() for version in stdout.strip().split("\n")[1:]]


def main():
    # with open('test.yml', 'r') as stream:
    #     questions = load(stream, Loader=Loader)
    # print(questions)

    questions = [
        {
            'type': 'text',
            'name': 'firstname',
            'message': "Specify your first name:",
        },
        {
            'type': 'text',
            'name': 'lastname',
            'message': "Specify your last name",
        },
        {
            'type': 'text',
            'name': 'lastname',
            'message': "What's your email address",
            'default': 'crazy@blabla.com'
        },
        {
            'type': 'select',
            'name': 'package_manager',
            'message': "Which package manager would you like to use",
            'choices': ['pipenv', 'poetry', 'conda'],
            'default': 'pipenv'
        },
        {
            'type': 'text',
            'name': 'shell',
            'message': "Specify the shell you use",
            'default': '/bin/bash'
        },
        {
            'type': 'text',
            'name': 'project_name',
            'message': "Specify the name of your project",
        },
        {
            'type': 'text',
            'name': 'project_slug',
            'message': "Specify the your projects slug name",
            'default': lambda x: x['project_name'].lower().replace(' ', '-')
        },
        {
            'type': 'text',
            'name': 'project_description',
            'message': "Give a short description of your project"
        },
        {
            'type': 'text',
            'name': 'project_homepage',
            'message': "Specify the homepage of your project",
            'validate': validate_url
        },
        {
            'type': 'text',
            'name': 'keywords',
            'message': "Specify up to five keywords for your project"
        },
        {
            'type': 'select',
            'name': 'license',
            'message': "Select a license for your project",
            'choices': ["MIT", "Apache-2.0", "BSD-3-Clause"],
            'default': 'MIT'
        },
        {
            'type': 'autocomplete',
            'name': 'python_version',
            'message': "Specify your python version",
            'choices': get_python_versions()
        },
        {
            'type': 'text',
            'name': 'package_version',
            'message': "Specify your package version",
            'default': "0.1.0",
            'validate': validate_package_version
        },
        {
            'type': 'checkbox',
            'name': 'services',
            'message': 'Which additional services would you like to use',
            'choices': [
                "Git-SCM",
                "Docker",
                "JupyterLab",
                "Continuous Integration (CI)"
            ]
        }
    ]

    git_questions = [
        {
            'type': 'select',
            'name': 'scm_server',
            'message': "Which source control server would you like to use",
            'choices': ["GitHub", "Gitlab", questionary.Separator(), "other"],
        },
        {
            'type': 'text',
            'name': 'scm_server_url',
            'message': "Specify the URL of your git server",
            'when': lambda x: x['scm_server'] == 'other'
        },
        {
            'type': 'text',
            'name': 'git_username',
            'message': "Specify your GitHub username",
            'when': lambda x: x['scm_server'] == 'GitHub'
        },
        {
            'type': 'text',
            'name': 'git_username',
            'message': "Specify your Gitlab username",
            'when': lambda x: x['scm_server'] == 'Gitlab'
        },
        {
            'type': 'password',
            'name': 'scm_token',
            'message': "Specify an access token for your chosen git server"
        },
    ]

    docker_questions = [
        {
            'type': 'select',
            'name': 'docker_registry',
            'message': "Which docker registry would you like to use",
            'choices': ["DockerHub", questionary.Separator(), "other"],
        },
        {
            'type': 'text',
            'name': 'docker_registry_url',
            'message': "Specify the URL of your docker registry",
            'when': lambda x: x['docker_registry'] == 'other'
        },
        {
            'type': 'password',
            'name': 'docker_token',
            'message': "Specify an access token for your registry",
        }
    ]

    ci_questions = [
         {
            'type': 'select',
            'name': 'ci_tool',
            'message': "Which CI tool would you like to use",
            'choices': ["Travis CI", "Gitlab CI", questionary.Separator(), "None"],
        },
    ]

    answers = questionary.prompt(questions)
    git_answers = None
    docker_answers = None
    ci_answers = None

    if 'Git-SCM' in answers["services"]:
        git_answers = questionary.prompt(git_questions)
    if 'Docker' in answers["services"]:
        docker_answers = questionary.prompt(docker_questions)
    if 'Continuous Integration (CI)' in answers["services"]:
        ci_answers = questionary.prompt(ci_questions)
    
    print(answers)
    print(git_answers)
    print(docker_answers)
    print(ci_answers)

    # answers = {}
    # for key, value in questions.items():
    #     quest = get_prompt(value)
    #     if 'depends_on' in value:
    #        print('Execute conditional')
    #        answers[key] = quest.skip_if(answers[value['depends_on']] is None).ask() 
    #     else:
    #         answers[key] = quest.ask()

    #firstname = questionary.text("Whats your first name?").ask()
    #response = questionary.confirm("Are you amazed?").skip_if(firstname is None).ask()

if __name__ == "__main__":
    main()