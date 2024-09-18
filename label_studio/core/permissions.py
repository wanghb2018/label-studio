"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging  # noqa: I001
from typing import Optional

from pydantic import BaseModel

import rules

logger = logging.getLogger(__name__)


class AllPermissions(BaseModel):
    organizations_create = 'organizations.create'
    organizations_view = 'organizations.view'
    organizations_change = 'organizations.change'
    organizations_delete = 'organizations.delete'
    organizations_invite = 'organizations.invite'
    projects_create = 'projects.create'
    projects_view = 'projects.view'
    projects_change = 'projects.change'
    projects_delete = 'projects.delete'
    tasks_create = 'tasks.create'
    tasks_view = 'tasks.view'
    tasks_change = 'tasks.change'
    tasks_delete = 'tasks.delete'
    data_manager_view = 'data_manager.view'
    data_manager_create = 'data_manager.create'
    data_manager_change = 'data_manager.change'
    data_manager_delete = 'data_manager.delete'
    annotations_create = 'annotations.create'
    annotations_view = 'annotations.view'
    annotations_change = 'annotations.change'
    annotations_delete = 'annotations.delete'
    actions_perform = 'actions.perform'
    predictions_any = 'predictions.any'
    avatar_any = 'avatar.any'
    labels_create = 'labels.create'
    labels_view = 'labels.view'
    labels_change = 'labels.change'
    labels_delete = 'labels.delete'
    models_create = 'models.create'
    models_view = 'models.view'
    models_change = 'models.change'
    models_delete = 'models.delete'
    model_provider_connection_create = 'model_provider_connection.create'
    model_provider_connection_view = 'model_provider_connection.view'
    model_provider_connection_change = 'model_provider_connection.change'
    model_provider_connection_delete = 'model_provider_connection.delete'


all_permissions = AllPermissions()


class ViewClassPermission(BaseModel):
    GET: Optional[str] = None
    PATCH: Optional[str] = None
    PUT: Optional[str] = None
    DELETE: Optional[str] = None
    POST: Optional[str] = None


def make_perm(name, pred, overwrite=False):
    if rules.perm_exists(name):
        if overwrite:
            rules.remove_perm(name)
        else:
            return
    rules.add_perm(name, pred)


for _, permission_name in all_permissions:
    if permission_name in [
        all_permissions.projects_view,
        all_permissions.tasks_view,
        all_permissions.data_manager_view,
        all_permissions.data_manager_change,
        all_permissions.labels_view,
        all_permissions.annotations_create,
        all_permissions.annotations_view,
        all_permissions.annotations_change,
        all_permissions.annotations_delete,
        all_permissions.organizations_change,
        all_permissions.organizations_view,
        all_permissions.avatar_any
    ]:
        make_perm(permission_name, rules.is_authenticated)
    elif permission_name in [
        all_permissions.labels_create,
        all_permissions.labels_change,
        all_permissions.labels_delete,
        all_permissions.tasks_delete,
        all_permissions.tasks_create,
        all_permissions.tasks_change,
        all_permissions.data_manager_create,
        all_permissions.data_manager_delete
    ]:
        make_perm(permission_name, rules.is_staff)
    else:
        make_perm(permission_name, rules.is_superuser)
