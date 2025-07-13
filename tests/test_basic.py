from engine_turbo.templates import TemplateEngine


def test_list_templates():
    engine = TemplateEngine("templates")
    templates = engine.list_templates()
    assert "saas-basic" in templates
