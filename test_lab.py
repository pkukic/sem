import os
import subprocess

# Get the directory where the script is located
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Loop through the test cases
for i in range(1, 16):
    print("#################################################################################################")
    print(f"Test {i}")

    test_input = os.path.join(ROOT_DIR, f"testovi/test_{i}/test.in")
    test_output = os.path.join(ROOT_DIR, f"testovi/test_{i}/test.out")
    
    # Run SemantickiAnalizator.py and capture its output
    with open(test_input, 'r') as infile:
        process = subprocess.run(
            ["python3", "SemantickiAnalizator.py"],
            input=infile.read(),
            text=True,
            capture_output=True
        )

    # Read the expected output
    with open(test_output, 'r') as expected_outfile:
        expected_output = expected_outfile.read()

    # Run the diff command to compare the actual output with the expected output
    diff_process = subprocess.run(
        ["diff", "-B"],
        input=process.stdout,
        text=True,
        capture_output=True
    )

    # Check if the diff output is empty (i.e., the outputs are the same)
    if diff_process.stdout == "":
        print("OK")
    else:
        print(diff_process.stdout)
