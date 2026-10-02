from loom.agents.translator import TranslatorAgent


def test_python2_to_python3_translation():
    translator = TranslatorAgent()

    legacy_code = 'print "Hello Legacy Loom"'

    modern_code = translator.translate_python2_to_python3(
        legacy_code
    )

    assert modern_code == 'print("Hello Legacy Loom")'