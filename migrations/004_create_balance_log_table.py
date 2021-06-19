"""Peewee migrations -- 001_create_user_table.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import peewee as pw

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql("""
    CREATE TABLE IF NOT EXISTS public.log (
        id int4 NOT NULL,
        login text NOT NULL,
        old_balance int4 NOT NULL,
        new_balance int4 NOT NULL,
        time timestamp DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE OR REPLACE FUNCTION log_balance() RETURNS TRIGGER AS
    $$
    BEGIN
        INSERT INTO log (id, login, old_balance, new_balance) VALUES (OLD.id, OLD.login, OLD.balance, NEW.balance);
        RETURN NEW;
    END
    $$
        LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS balance_log ON public.discord;
    
    CREATE TRIGGER balance_log 
        AFTER UPDATE ON public.discord
        FOR EACH ROW
        WHEN (OLD.balance IS DISTINCT FROM NEW.balance)
        EXECUTE FUNCTION log_balance()
    """)


def rollback(migrator, database, fake=False, **kwargs):
    migrator.sql("""
    DROP TABLE IF EXISTS public.log;
    """)

