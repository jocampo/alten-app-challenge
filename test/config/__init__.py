from yaml import safe_load

config_values = None


try:
    with open("./test/config/conf.yaml", "r", encoding="utf-8") as config_file:
        config_values = safe_load(config_file)
        config_file.close()
except FileNotFoundError:
    raise Exception(
        "Please copy the file /test/config/conf.yaml.TEMPLATE into /test/config/conf.yaml and populate it with a test "
        "db url in order to run tests"
    )

MOCK_DATABASE_URL = config_values.get("test_database_url", "")
