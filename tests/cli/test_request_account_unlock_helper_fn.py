import pytest
import click
from click.testing import CliRunner

from geth.accounts import create_new_account

from web3.utils.string import force_text

from populus.utils.accounts import (
    is_account_locked,
)
from populus.utils.cli import (
    request_account_unlock,
)
from populus.project import Project


def test_request_account_unlock_with_correct_password(project_dir):
    project = Project()
    chain = project.get_chain('temp')

    # create 3 new accounts
    account = force_text(
        create_new_account(chain.geth.data_dir, b'a-test-password')
    )

    @click.command()
    def wrapper():
        request_account_unlock(chain, account, None)

    with chain:
        assert is_account_locked(chain.web3, account)

        runner = CliRunner()
        result = runner.invoke(wrapper, [], input="a-test-password\n")

        assert result.exit_code == 0
        assert not is_account_locked(chain.web3, account)


def test_request_account_unlock_with_bad_password(project_dir):
    project = Project()
    chain = project.get_chain('temp')

    # create 3 new accounts
    account = force_text(
        create_new_account(chain.geth.data_dir, b'a-test-password')
    )

    @click.command()
    def wrapper():
        request_account_unlock(chain, account, None)

    with chain:
        assert is_account_locked(chain.web3, account)

        runner = CliRunner()
        result = runner.invoke(wrapper, [], input="bad-password\n")

        assert result.exit_code != 0
        assert is_account_locked(chain.web3, account)
