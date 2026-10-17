# D:\AI-Tools\convermem\tests\test_cli.py
from click.testing import CliRunner
from convermem.cli import main

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "ConverMem" in result.output
