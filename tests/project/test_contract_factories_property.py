import pytest

from populus.project import Project


def test_project_contract_factories_property(project_dir, write_project_file,
                                             MATH):
    write_project_file('contracts/Math.sol', MATH['source'])

    project = Project()
    with project.get_chain('testrpc') as chain:
        assert len(chain.contract_factories.Math.abi) == len(MATH['abi'])
        assert len(chain.contract_factories.Math.code) > 2
        assert len(chain.contract_factories.Math.code_runtime) > 2
