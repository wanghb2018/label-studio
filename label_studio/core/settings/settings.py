import os


def get_label_projects():
    projects = os.environ.get('LABEL_PROJECTS')
    if not projects:
        return []
    return list(map(int, projects.split(',')))