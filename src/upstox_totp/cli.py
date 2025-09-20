"""CLI for Upstox TOTP."""

import os

import click

from upstox_totp.client import UpstoxTOTP


@click.group()
def cli() -> None:
    """
    CLI for Upstox TOTP - Automate Upstox API authentication.

    This tool helps you generate access tokens for Upstox API using TOTP authentication.

    Required Environment Variables:

    \b
    • UPSTOX_USERNAME       - Your Upstox username
    • UPSTOX_PASSWORD       - Your Upstox password
    • UPSTOX_PIN_CODE       - Your Upstox PIN code
    • UPSTOX_TOTP_SECRET    - Your TOTP secret key
    • UPSTOX_CLIENT_ID      - Your Upstox app client ID
    • UPSTOX_CLIENT_SECRET  - Your Upstox app client secret
    • UPSTOX_REDIRECT_URI   - Your app redirect URI
    • UPSTOX_DEBUG          - Enable debug mode (optional, default: false)

    You can also create a .env file with these variables.

    Examples:

    \b
    # Generate access token
    upstox_cli generate-token

    # Show help for specific command
    upstox_cli generate-token --help
    """
    pass


@click.command("generate-token")
def generate_token() -> None:
    """
    Generate access token for Upstox API.

    This command will:

    \b
    1. Load your credentials from environment variables or .env file
    2. Generate a TOTP code using your secret
    3. Authenticate with Upstox servers
    4. Fetch and display your access token

    The generated token can be used to make authenticated API calls to Upstox.

    Examples:

    \b
    # Generate token with default settings
    upstox_cli generate-token

    Make sure all required environment variables are set before running this command.
    Use 'upstox_cli --help' to see the list of required variables.
    """
    try:
        upx: UpstoxTOTP = UpstoxTOTP()
        response = upx.app_token.get_access_token()

        if response.success and response.data:
            click.echo("\n🎉 Access token generated successfully!")
            click.echo(f"\nToken Details:")
            click.echo(f"Access Token: {response.data.access_token}")
            click.echo(f"User ID: {response.data.user_id}")
            click.echo(f"User Name: {response.data.user_name}")
            click.echo(f"User Type: {response.data.user_type}")
            click.echo(f"Broker: {response.data.broker}")
            click.echo(f"Email: {response.data.email}")
            click.echo(f"Products: {', '.join(response.data.products)}")
            click.echo(f"Exchanges: {', '.join(response.data.exchanges)}")
            click.echo(f"Is Active: {response.data.is_active}")

            if response.data.extended_token:
                click.echo(f"Extended Token: {response.data.extended_token}")

            click.echo("\n💡 You can now use this access token to make authenticated API calls to Upstox.")
        else:
            click.echo(f"\n Failed to generate access token", err=True)
            if response.error:
                click.echo(f"Error details: {response.error}", err=True)
            raise click.Abort()

    except Exception as e:
        click.echo(f"\n Error generating access token: {e}", err=True)
        click.echo("\n💡 Make sure all required environment variables are set.", err=True)
        click.echo("   Use 'upstox_cli --help' to see the list of required variables.", err=True)
        raise click.Abort()


@click.command("check-env")
def check_env() -> None:
    """
    Check if all required environment variables are set.

    This command validates that all necessary environment variables are properly
    configured before attempting to generate tokens.

    Examples:

    \b
    # Check environment setup
    upstox_cli check-env
    """
    from dotenv import load_dotenv

    load_dotenv()

    required_vars = ["UPSTOX_USERNAME", "UPSTOX_PASSWORD", "UPSTOX_PIN_CODE", "UPSTOX_TOTP_SECRET", "UPSTOX_CLIENT_ID", "UPSTOX_CLIENT_SECRET", "UPSTOX_REDIRECT_URI"]

    optional_vars = ["UPSTOX_DEBUG"]

    click.echo("🔍 Checking environment variables...\n")

    missing_required = []
    present_required = []

    for var in required_vars:
        value = os.getenv(var)
        if value:
            present_required.append(var)

            if "SECRET" in var or "PASSWORD" in var:
                display_value = f"{value[:4]}{'*' * (len(value) - 4)}" if len(value) > 4 else "****"
            else:
                display_value = value[:20] + "..." if len(value) > 20 else value
            click.echo(f"{var}: {display_value}")
        else:
            missing_required.append(var)
            click.echo(f" {var}: Not set", err=True)

    click.echo("\nOptional variables:")
    for var in optional_vars:
        value = os.getenv(var, "false")
        click.echo(f"{var}: {value}")

    click.echo(f"\nSummary:")
    click.echo(f"   Required variables: {len(present_required)}/{len(required_vars)} set")

    if missing_required:
        click.echo(f"\n Missing required variables:")
        for var in missing_required:
            click.echo(f"   • {var}")
        click.echo(f"\n💡 Set these variables in your environment or .env file before running 'generate-token'")
        raise click.Abort()
    else:
        click.echo(f"\n🎉 All required environment variables are set!")
        click.echo(f"   You can now run 'upstox_cli generate-token' to get your access token.")


cli.add_command(generate_token)
cli.add_command(check_env)
