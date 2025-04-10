import click
from vault import generate_key, encrypt_data

# Create a Click command group to support multiple subcommands (init, add, get, etc.)
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
    Prompts the user for a master password, which is used to derive the encryption key.
    The vault is saved as an AES-encrypted file (vault.json.enc).
    """
    key = generate_key(master)  # Derive a 256-bit encryption key from the password
    encrypted = encrypt_data({}, key)  # Encrypt an empty vault (no credentials yet)

    # Save the encrypted vault to a file
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
    Adds a new credential (site, username, password) to the encrypted vault.
    Prompts the user for the master password, decrypts the vault, appends the new entry,
    then re-encrypts and saves it securely.
    """
    from vault import generate_key, encrypt_data, decrypt_data
    import os

    key = generate_key(master)  # Derive encryption key from master password

    try:
        # Ensure the vault file exists before proceeding
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        # Load and decrypt the existing vault
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        # Add new credentials to the vault under the provided site
        data[site] = {
            "username": username,
            "password": password
        }

        # Re-encrypt the updated vault and overwrite the previous file
        with open("vault.json.enc", "wb") as f:
            f.write(encrypt_data(data, key))

        click.echo(f"✅ Credentials for '{site}' added to vault!")

    except Exception as e:
        # Handle decryption failures or file corruption
        click.echo(f"❌ Error: {e}")


# ---------------------
# GET COMMAND
# ---------------------

@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
def get(master, site):
    """
    Retrieves credentials for a given site from the encrypted vault.
    Requires the master password to decrypt and access the data.
    """
    from vault import generate_key, decrypt_data
    import os

    key = generate_key(master)  # Derive encryption key from master password

    try:
        # Ensure the vault file exists
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        # Load and decrypt the vault
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        # Check if the site exists in the vault
        if site not in data:
            click.echo(f"❌ No credentials found for '{site}'.")
            return

        # Extract and display the credentials
        creds = data[site]
        click.echo("🔍 Credentials found:")
        click.echo(f"  👤 Username: {creds['username']}")
        click.echo(f"  🔑 Password: {creds['password']}")

    except Exception as e:
        # Handle decryption errors or file corruption
        click.echo(f"❌ Error: {e}")

# ---------------------
# LIST COMMAND
# ---------------------

@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def list(master):
    """
    Lists all saved sites in the encrypted vault.
    Allows users to quickly see which accounts are stored.
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
    Prompts for master password, confirms existence, and removes the entry.
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
    Requires the master password to decrypt and access the vault.
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

        # Copy password to clipboard
        pyperclip.copy(data[site]["password"])
        click.echo(f"📋 Password for '{site}' copied to clipboard!")

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# Entry point for the CLI tool
# Ensures that commands are only run when the script is executed directly
if __name__ == '__main__':
    cli()
