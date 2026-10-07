from loom.sandbox.docker_runner import DockerRunner


def test_docker_runner():
    runner = DockerRunner()

    result = runner.run_python2(
        "examples/python2/legacy.py",
        "10 20 30\n",
    )

    assert result.success is True
    assert "60" in result.output