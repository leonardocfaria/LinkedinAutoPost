from dynaconf import Dynaconf

config = Dynaconf(
    root_path="../..",
    envvar_prefix="LAP",  # export envvars with `export DYNACONF_FOO=bar`.
    settings_files=["settings.toml", ".secrets.toml"],  # Load files in the given order.
)
