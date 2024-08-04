import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, check=True)
    return result


def main():
    # Run Alembic migrations
    run_command("alembic upgrade head")

    # Run data population script
    run_command("python populate_db.py")


if __name__ == "__main__":
    main()
