# Generated by Django 3.2.25 on 2024-07-31 16:38

from django.conf import settings
from django.db import migrations, models
from django.db.migrations.operations.special import RunSQL
from django.db.migrations.operations.base import Operation
from django.db import connection
from core.redis import start_job_async_or_sync
from core.models import AsyncMigrationStatus
import logging
logger = logging.getLogger(__name__)


IS_SQLITE = settings.DJANGO_DB == settings.DJANGO_DB_SQLITE
migration_name = '0017_auto_20240731_1638'

def create_index_sql(table_name, index_name, column_name):
    return f"""
    CREATE INDEX CONCURRENTLY IF NOT EXISTS "{index_name}" ON "{table_name}" ("{column_name}");
    """

def create_fk_sql(table_name, constraint_name, column_name, referenced_table, referenced_column):
    return f"""
    ALTER TABLE "{table_name}" DROP CONSTRAINT IF EXISTS "{constraint_name}";
    ALTER TABLE "{table_name}" ADD CONSTRAINT "{constraint_name}" FOREIGN KEY ("{column_name}") REFERENCES "{referenced_table}" ("{referenced_column}") DEFERRABLE INITIALLY DEFERRED;
    """

def drop_index_sql(table_name, index_name, column_name):
    return f"""
    DROP INDEX CONCURRENTLY IF EXISTS "{index_name}";
    """

tables = [
    {
        "model_name": "azureblobexportstoragelink",
        "table_name": "io_storages_azureblobexportstoragelink",
        "index_name": "io_storages_azureblobexportstoragelink_annotation_id_6cc15c83",
        "fk_constraint": "io_storages_azureblo_annotation_id_6cc15c83_fk_task_comp",
        "column_name": "annotation_id"
    },
    {
        "model_name": "gcsexportstoragelink",
        "table_name": "io_storages_gcsexportstoragelink",
        "index_name": "io_storages_gcsexportstoragelink_annotation_id_2df715a6",
        "fk_constraint": "io_storages_gcsexpor_annotation_id_2df715a6_fk_task_comp",
        "column_name": "annotation_id"
    },
    {
        "model_name": "localfilesexportstoragelink",
        "table_name": "io_storages_localfilesexportstoragelink",
        "index_name": "io_storages_localfilesexportstoragelink_annotation_id_fc4f9825",
        "fk_constraint": "io_storages_localfil_annotation_id_fc4f9825_fk_task_comp",
        "column_name": "annotation_id"
    },
    {
        "model_name": "redisexportstoragelink",
        "table_name": "io_storages_redisexportstoragelink",
        "index_name": "io_storages_redisexportstoragelink_annotation_id_8547e508",
        "fk_constraint": "io_storages_redisexp_annotation_id_8547e508_fk_task_comp",
        "column_name": "annotation_id"
    },
    {
        "model_name": "s3exportstoragelink",
        "table_name": "io_storages_s3exportstoragelink",
        "index_name": "io_storages_s3exportstoragelink_annotation_id_729994fe",
        "fk_constraint": "io_storages_s3export_annotation_id_729994fe_fk_task_comp",
        "column_name": "annotation_id"
    }
]


def forward_migration(migration_name):
    migration = AsyncMigrationStatus.objects.create(
        name=migration_name,
        status=AsyncMigrationStatus.STATUS_STARTED,
    )
    logger.debug(
        f'Start async migration {migration_name}'
    )

    # Get db cursor
    cursor = connection.cursor()
    for table in tables:
        index_sql = create_index_sql(table['table_name'], table['index_name'], table['column_name'])
        fk_sql = create_fk_sql(table['table_name'], table['fk_constraint'], table['column_name'], "task_completion",
                               "id")

        # Run index_sql
        cursor.execute(index_sql)
        cursor.execute(fk_sql)

    migration.status = AsyncMigrationStatus.STATUS_FINISHED
    migration.save()
    logger.debug(
        f'Async migration {migration_name} complete'
    )

def reverse_migration(migration_name):
    migration = AsyncMigrationStatus.objects.create(
        name=migration_name,
        status=AsyncMigrationStatus.STATUS_STARTED,
    )
    logger.debug(
        f'Start async migration {migration_name}'
    )

    # Get db cursor
    cursor = connection.cursor()
    for table in tables:
        reverse_sql = drop_index_sql(table['table_name'], table['index_name'], table['column_name'])
        # Run reverse_sql
        cursor.execute(reverse_sql)

    migration.status = AsyncMigrationStatus.STATUS_FINISHED
    migration.save()
    logger.debug(
        f'Async migration {migration_name} complete'
    )


def forwards(apps, schema_editor):
    # Dispatch migrations to rqworkers
    start_job_async_or_sync(forward_migration, migration_name=migration_name)


def backwards(apps, schema_editor):
    start_job_async_or_sync(reverse_migration, migration_name=migration_name)


def get_operations():
    if not IS_SQLITE:
        return [
            migrations.RunPython(forwards, backwards),
        ]

    # Use standard migration for SQLITE
    for table in tables:
        operations.append(
            migrations.AlterField(
                model_name=table['model_name'],
                name='annotation',
                field=models.ForeignKey(on_delete=models.deletion.CASCADE,
                                        related_name=table['table_name'],
                                        to='tasks.annotation'),
            ),
        )


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('tasks', '0047_merge_20240318_2210'),
        ('io_storages', '0016_add_aws_sse_kms_key'),
    ]

    operations = get_operations()

