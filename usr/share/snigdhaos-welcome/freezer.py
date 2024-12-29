import subprocess

def create_requirements_file(filename="requirements.txt"):
    try:
        # Run the pip freeze command and capture the output
        result = subprocess.run(
            ["pip", "freeze"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            # Write the output to the requirements.txt file
            with open(filename, "w") as file:
                file.write(result.stdout)
            print(f"{filename} created successfully!")
        else:
            print("Error generating requirements:", result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to create the requirements.txt file
create_requirements_file()
