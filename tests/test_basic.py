def test_importable():
    import pycodemark

    assert hasattr(pycodemark, "__name__")
