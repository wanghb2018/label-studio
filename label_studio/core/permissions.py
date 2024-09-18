"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging  # noqa: I001
from typing import Optional

from pydantic import BaseModel

import rules

logger = logging.getLogger(__name__)


class AllPermissions(BaseModel):
    organizations_create: str = 'organizations.create'
    organizations_view: str = 'organizations.view'
    organizations_change: str = 'organizations.change'
    organizations_delete: str = 'organizations.delete'
    organizations_invite: str = 'organizations.invite'
    projects_create: str = 'projects.create'
    projects_view: str = 'projects.view'
    projects_change: str = 'projects.change'
    projects_delete: str = 'projects.delete'
    tasks_create: str = 'tasks.create'
    tasks_view: str = 'tasks.view'
    tasks_change: str = 'tasks.change'
    tasks_delete: str = 'tasks.delete'
    data_manager_view: str = 'data_manager.view'
    data_manager_create: str = 'data_manager.create'
    data_manager_change: str = 'data_manager.change'
    data_manager_delete: str = 'data_manager.delete'
    annotations_create: str = 'annotations.create'
    annotations_view: str = 'annotations.view'
    annotations_change: str = 'annotations.change'
    annotations_delete: str = 'annotations.delete'
    actions_perform: str = 'actions.perform'
    predictions_any: str = 'predictions.any'
    avatar_any: str = 'avatar.any'
    labels_create: str = 'labels.create'
    labels_view: str = 'labels.view'
    labels_change: str = 'labels.change'
    labels_delete: str = 'labels.delete'
    models_create: str = 'models.create'
    models_view: str = 'models.view'
    models_change: str = 'models.change'
    models_delete: str = 'models.delete'
    model_provider_connection_create: str = 'model_provider_connection.create'
    model_provider_connection_view: str = 'model_provider_connection.view'
    model_provider_connection_change: str = 'model_provider_connection.change'
    model_provider_connection_delete: str = 'model_provider_connection.delete'


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
