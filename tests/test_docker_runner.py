from loom.sandbox.docker_runner import DockerRunner


def test_docker_runner():
    runner = DockerRunner()

    result = runner.run_python2("docker/legacy.py")

    assert result.success is True
    assert "60" in result.output
    assert "Hello, Legacy Loom" in result.output
