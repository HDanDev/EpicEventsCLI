# import pytest
# from click.testing import CliRunner
# from crm.cli.auth import login, logout
# from crm.services.auth import keyring
# from tests.test_context_db import test_db, test_manager_email, password

# @pytest.fixture
# def runner():
#     """Provide Click CLI test runner."""
#     return CliRunner()

# def test_login_command_success(runner, mocker):
#     """Test successful CLI login."""
#     mocker.patch("crm.services.auth.login", return_value=("Test User", None))

#     result = runner.invoke(login, ["--email", "test@email.com", "--password", "password123"])

#     assert result.exit_code == 0
#     assert "✅ Logged in as" in result.output

# def test_login_command_failure(runner, mocker):
#     """Test CLI login failure."""
#     mocker.patch("crm.services.auth.login", return_value=(None, "❌ Invalid email or password"))

#     result = runner.invoke(login, ["--email", "wrong@email.com", "--password", "wrongpassword"])

#     assert result.exit_code == 0
#     assert "❌ Invalid email or password" in result.output

# def test_logout_command_success(runner, mocker):
#     """Test successful CLI logout."""
#     mocker.patch("crm.services.auth.logout", return_value=None)

#     result = runner.invoke(logout)

#     assert result.exit_code == 0
#     assert "✅ Successfully logged out!" in result.output

# def test_logout_command_failure(runner, mocker):
#     """Test CLI logout failure (e.g., no active session)."""
#     mocker.patch("crm.services.auth.logout", return_value="⚠️ No active session found.")

#     result = runner.invoke(logout)

#     assert result.exit_code == 0
#     assert "⚠️ No active session found." in result.output
