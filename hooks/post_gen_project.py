import os
import shutil

def append_to_gitignore_file(s):
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(s)
        gitignore_file.write(os.linesep)

def remove_docker_files():
    filenames = ['Dockerfile', '.dockerignore']
    for filename in filenames:
        os.remove(filename)

def remove_jupyter_files():
    filenames = []
    directories = ['notebooks']

    for directory in directories:
        shutil.rmtree(f'./{directory}')

    for filename in filenames:
        os.remove(filename)

def remove_travis_files():
    filenames = ['.travis.yml']
    for filename in filenames:
        os.remove(filename)

def main():
    if "{{ cookiecutter.use_docker }}".lower() == "no":
        remove_docker_files()
    if "{{ cookiecutter.use_jupyterlab }}".lower() == "no":
        remove_jupyter_files()
    if "{{ cookiecutter.ci_tool }}".lower() != "travis":
        remove_travis_files()

if __name__ == "__main__":
    main()