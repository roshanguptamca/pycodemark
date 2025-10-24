def test_importable():
    import codemark
    assert hasattr(codemark, "__name__")
