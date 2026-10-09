import sys

def test_imports():
    print("=" * 50)
    print("SIGN LANGUAGE RECOGNITION - SETUP TEST")
    print("=" * 50)
    print(f"\nPython version: {sys.version.split()[0]}\n")

    modules_to_test = [
        ("cv2", "OpenCV"),
        ("mediapipe", "MediaPipe"),
        ("tensorflow", "TensorFlow"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("sklearn", "Scikit-learn"),
        ("matplotlib", "Matplotlib"),
        ("streamlit", "Streamlit"),
        ("pyttsx3", "pyttsx3"),
    ]

    failed_modules = []

    for mod_name, display_name in modules_to_test:
        try:
            __import__(mod_name)
            print(f"[OK] {display_name}")
        except Exception as e:
            print(f"[FAILED] {display_name}")
            print(f"   Error Details: {e}")
            failed_modules.append((display_name, str(e)))

    print("\n" + "=" * 50)
    if not failed_modules:
        print("ALL REQUIRED LIBRARIES ARE WORKING")
        print("=" * 50)
        return True
    else:
        print("SETUP FAILED: THE FOLLOWING LIBRARIES COULD NOT BE IMPORTED:")
        for display_name, err in failed_modules:
            print(f" - {display_name}: {err}")
        print("=" * 50)
        return False

if __name__ == "__main__":
    success = test_imports()
    if not success:
        sys.exit(1)
