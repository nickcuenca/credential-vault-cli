import click
from vault import generate_key, encrypt_data

# Define a group of CLI commands (init, add, get, etc.)
@click.group()
def cli():
    pass

# ---------------------
# INIT COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def init(master):
    """
    Initializes a new encrypted credential vault.
    The master password is used to derive an encryption key,
    which is used to encrypt an empty dictionary and save it to disk.
    """
    key = generate_key(master)  # Derive a consistent encryption key from the password
    encrypted = encrypt_data({}, key)  # Encrypt an empty dictionary

    # Save encrypted data to file
    with open("vault.json.enc", "wb") as f:
        f.write(encrypted)

    click.echo("🔐 Vault initialized and encrypted!")


# ---------------------
# ADD COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
@click.option('--username', prompt="Username")
@click.option('--password', prompt="Password", hide_input=True, confirmation_prompt=True)
def add(master, site, username, password):
    """
    Adds credentials for a given site to the encrypted vault.
    If the vault exists, it decrypts, updates it, re-encrypts, and saves it.
    """
    from vault import generate_key, encrypt_data, decrypt_data
    import os

    key = generate_key(master)

    try:
        # Check that vault exists
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        # Load and decrypt vault
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        # Add the new site credentials
        data[site] = {
            "username": username,
            "password": password
        }

        # Re-encrypt and save the updated vault
        with open("vault.json.enc", "wb") as f:
            f.write(encrypt_data(data, key))

        click.echo(f"✅ Credentials for '{site}' added to vault!")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# GET COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
def get(master, site):
    """
    Retrieves and displays credentials for a given site from the encrypted vault.
    """
    from vault import generate_key, decrypt_data
    import os

    key = generate_key(master)

    try:
        # Validate vault presence
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        # Decrypt vault
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        # Display credentials
        if site not in data:
            click.echo(f"❌ No credentials found for '{site}'.")
            return

        creds = data[site]
        click.echo("🔍 Credentials found:")
        click.echo(f"  👤 Username: {creds['username']}")
        click.echo(f"  🔑 Password: {creds['password']}")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# LIST COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def list(master):
    """
    Lists all saved site names stored in the encrypted vault.
    """
    from vault import generate_key, decrypt_data
    import os

    key = generate_key(master)

    try:
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if not data:
            click.echo("⚠️ Vault is empty. Add some credentials with `add`.")
            return

        click.echo("🔐 Stored Sites:")
        for site in data:
            click.echo(f"  - {site}")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# DELETE COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
def delete(master, site):
    """
    Deletes credentials for a given site from the encrypted vault.
    """
    from vault import generate_key, encrypt_data, decrypt_data
    import os

    key = generate_key(master)

    try:
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if site not in data:
            click.echo(f"❌ No credentials found for '{site}'.")
            return

        del data[site]

        with open("vault.json.enc", "wb") as f:
            f.write(encrypt_data(data, key))

        click.echo(f"🗑️ Credentials for '{site}' deleted from vault.")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# COPY COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
def copy(master, site):
    """
    Copies the password for a given site to the clipboard.
    """
    from vault import generate_key, decrypt_data
    import pyperclip
    import os

    key = generate_key(master)

    try:
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if site not in data:
            click.echo(f"❌ No credentials found for '{site}'.")
            return

        pyperclip.copy(data[site]["password"])
        click.echo(f"📋 Password for '{site}' copied to clipboard!")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# EXPORT COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def export(master):
    """
    Decrypts and exports all credentials to a plaintext file (vault_export.txt).
    NOTE: File is not encrypted — store it safely.
    """
    from vault import generate_key, decrypt_data
    import os

    key = generate_key(master)

    try:
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if not data:
            click.echo("⚠️ Vault is empty. Nothing to export.")
            return

        with open("vault_export.txt", "w", encoding="utf-8") as f:
            for site, creds in data.items():
                f.write(f"Site: {site}\n")
                f.write(f"  Username: {creds['username']}\n")
                f.write(f"  Password: {creds['password']}\n")
                f.write("\n")

        click.echo("✅ Vault successfully exported to 'vault_export.txt'.")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# MAIN ENTRY POINT
# ---------------------
if __name__ == '__main__':
    cli()
