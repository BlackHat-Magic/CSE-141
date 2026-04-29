if __name__ == "__main__":
    import test_lab4

    tests = sorted(f for f in dir(test_lab4) if f.startswith("test_"))
    passed = 0
    for t in tests:
        try:
            getattr(test_lab4, t)()
            print(f"PASS: {t}")
            passed += 1
        except Exception as e:
            print(f"FAIL: {t}  ({e})")
    print()
    print(f"Results: {passed}/{len(tests)} passed")
