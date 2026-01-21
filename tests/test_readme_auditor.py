from opendevtoolkit.plugins.readme_auditor import audit_readme


def test_audit_readme_basics():
    md = """# Title

## Install
pip install x

## Usage
do thing

## License
MIT

![img](x.png)
"""
    findings = audit_readme(md, min_sections=3)
    assert any(name == "Title header" and ok for name, ok, _ in findings)
    assert any(name == "Install instructions" and ok for name, ok, _ in findings)
    assert any(name == "Usage section" and ok for name, ok, _ in findings)
    assert any(name == "License mentioned" and ok for name, ok, _ in findings)
    assert any(name == "Screenshot or image" and ok for name, ok, _ in findings)
