import click
import traceback
from vault import generate_key, encrypt_data, is_vault_locked, update_last_access

@click.group()
def cli():
    """Credential Vault CLI - Securely store, retrieve, and manage your passwords."""
    pass

# ---------------------
# INIT COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def init(master):
    """Initialize a new encrypted credential vault."""
    import os

    if os.path.exists("vault.json.enc"):
        update_last_access()
        click.echo("✅ Vault already exists. Session refreshed.")
        return

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
    """Add new credentials for a website to your encrypted vault."""
    from vault import encrypt_data, decrypt_data, check_password_strength
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

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
        traceback.print_exc()

# ---------------------
# GET COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
def get(master, site):
    """Retrieve credentials for a given site."""
    from vault import decrypt_data
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

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
        traceback.print_exc()

# ---------------------
# LIST COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def list(master):
    """List all stored sites in your vault."""
    from vault import decrypt_data
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

        if not data:
            click.echo("⚠️ Vault is empty. Add some credentials with `add`.")
            return

        click.echo("🔐 Stored Sites:")
        for site in data:
            click.echo(f"  - {site}")
        update_last_access()

    except Exception as e:
        click.echo(f"❌ Error: {e}")
        traceback.print_exc()

# ---------------------
# DELETE COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
def delete(master, site):
    """Delete credentials for a given site."""
    from vault import encrypt_data, decrypt_data
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

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
        traceback.print_exc()

# ---------------------
# COPY COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
def copy(master, site):
    """Copy a password to the clipboard for a given site."""
    from vault import decrypt_data
    import pyperclip
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

        if site not in data:
            click.echo(f"❌ No credentials found for '{site}'.")
            return

        pyperclip.copy(data[site]["password"])
        click.echo(f"📋 Password for '{site}' copied to clipboard!")
        update_last_access()

    except Exception as e:
        click.echo(f"❌ Error: {e}")
        traceback.print_exc()

# ---------------------
# EXPORT COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
def export(master):
    """Export all credentials to a plaintext file."""
    from vault import decrypt_data
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

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
        traceback.print_exc()

# ---------------------
# GENERATE PASSWORD COMMAND
# ---------------------
@cli.command()
@click.option('--length', default=16, prompt="Password Length")
@click.option('--copy', is_flag=True, help="Copy password to clipboard")
def generate(length, copy):
    """Generate a secure random password."""
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
# EDIT COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--site', prompt="Site")
@click.option('--new_username', prompt="New Username", default="", show_default=False)
@click.option('--new_password', prompt="New Password", hide_input=True, confirmation_prompt=True, default="", show_default=False)
def edit(master, site, new_username, new_password):
    """Edit credentials for a site."""
    from vault import encrypt_data, decrypt_data, check_password_strength
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

        if site not in data:
            click.echo(f"❌ No credentials found for '{site}'.")
            return

        if new_username:
            data[site]["username"] = new_username

        if new_password:
            data[site]["password"] = new_password
            strength = check_password_strength(new_password)
            click.echo(f"🧠 New Password Strength: {strength}")

        with open("vault.json.enc", "wb") as f:
            f.write(encrypt_data(data, key))

        click.echo(f"✏️ Credentials for '{site}' updated.")
        update_last_access()

    except Exception as e:
        click.echo(f"❌ Error: {e}")
        traceback.print_exc()

# ---------------------
# SEARCH COMMAND
# ---------------------
@cli.command()
@click.option('--master', prompt=True, hide_input=True)
@click.option('--query', prompt="Search query")
def search(master, query):
    """Search for sites in the vault matching a query."""
    from vault import decrypt_data
    import os

    key = generate_key(master)

    try:
        with open("vault.json.enc", "rb") as f:
            encrypted_data = f.read()
        data = decrypt_data(encrypted_data, key)

        if is_vault_locked():
            click.echo("🔒 Vault session expired. Session refreshed.")
        else:
            click.echo("🔓 Vault unlocked.")

        update_last_access()

        matches = {site: creds for site, creds in data.items() if query.lower() in site.lower()}
        if not matches:
            click.echo("🔎 No matches found.")
            return

        click.echo("🔍 Matching Results:")
        for site, creds in matches.items():
            click.echo(f"  🌐 Site: {site}")
            click.echo(f"     👤 Username: {creds['username']}")
            click.echo(f"     🔑 Password: {creds['password']}\n")

    except Exception as e:
        click.echo(f"❌ Error: {e}")
        traceback.print_exc()


# ---------------------
# HELP ENTRY
# ---------------------

@cli.command()
def help():
    """Show available commands."""
    import subprocess
    subprocess.run(["python", "cli.py", "--help"])


# ---------------------
# MAIN ENTRY
# ---------------------
if __name__ == '__main__':
    cli()
