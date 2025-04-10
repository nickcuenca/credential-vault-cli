import click
from vault import generate_key, encrypt_data, is_vault_locked, update_last_access

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
    """
    key = generate_key(master)
    encrypted = encrypt_data({}, key)

    with open("vault.json.enc", "wb") as f:
        f.write(encrypted)

    update_last_access()
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
    """
    from vault import generate_key, encrypt_data, decrypt_data, check_password_strength
    import os

    if is_vault_locked():
        click.echo("🔒 Vault session expired. Please re-enter or re-initialize.")
        return

    key = generate_key(master)

    try:
        if not os.path.exists("vault.json.enc"):
            click.echo("❌ Vault not initialized. Run `init` first.")
            return

        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        data[site] = {
            "username": username,
            "password": password
        }

        with open("vault.json.enc", "wb") as f:
            f.write(encrypt_data(data, key))

        strength = check_password_strength(password)
        click.echo(f"✅ Credentials for '{site}' added to vault!")
        click.echo(f"🧠 Password Strength: {strength}")
        update_last_access()

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
    Retrieves and displays credentials for a given site.
    """
    from vault import generate_key, decrypt_data
    import os

    if is_vault_locked():
        click.echo("🔒 Vault session expired. Please re-enter or re-initialize.")
        return

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

        creds = data[site]
        click.echo("🔍 Credentials found:")
        click.echo(f"  👤 Username: {creds['username']}")
        click.echo(f"  🔑 Password: {creds['password']}")
        update_last_access()

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# LIST COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def list(master):
    """
    Lists all saved site names.
    """
    from vault import generate_key, decrypt_data
    import os

    if is_vault_locked():
        click.echo("🔒 Vault session expired. Please re-enter or re-initialize.")
        return

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
        update_last_access()

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
    Deletes credentials for a given site from the vault.
    """
    from vault import generate_key, encrypt_data, decrypt_data
    import os

    if is_vault_locked():
        click.echo("🔒 Vault session expired. Please re-enter or re-initialize.")
        return

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
        update_last_access()

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
    Copies the password for a given site to clipboard.
    """
    from vault import generate_key, decrypt_data
    import pyperclip
    import os

    if is_vault_locked():
        click.echo("🔒 Vault session expired. Please re-enter or re-initialize.")
        return

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
        update_last_access()

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# EXPORT COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def export(master):
    """
    Exports all credentials to a plaintext file.
    """
    from vault import generate_key, decrypt_data
    import os

    if is_vault_locked():
        click.echo("🔒 Vault session expired. Please re-enter or re-initialize.")
        return

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
                f.write(f"  Password: {creds['password']}\n\n")

        click.echo("✅ Vault successfully exported to 'vault_export.txt'.")
        update_last_access()

    except Exception as e:
        click.echo(f"❌ Error: {e}")


# ---------------------
# GENERATE COMMAND
# ---------------------
@cli.command()
@click.option('--length', default=16, prompt="Password Length", help="Length of the generated password")
@click.option('--copy', is_flag=True, help="Copy generated password to clipboard")
def generate(length, copy):
    """
    Generates a secure password and optionally copies it.
    """
    import string
    import secrets
    import pyperclip
    from vault import check_password_strength

    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))

    click.echo(f"🔐 Generated Password: {password}")
    click.echo(f"🧠 Password Strength: {check_password_strength(password)}")

    if copy:
        pyperclip.copy(password)
        click.echo("📋 Password copied to clipboard!")


# ---------------------
# MAIN ENTRY POINT
# ---------------------
if __name__ == '__main__':
    cli()