from upstox_totp import UpstoxTOTP
from upstox_totp.models import AccessTokenResponse

# Initialize client (auto-loads from .env or environment variables)
# Alternatively, you can use the CLI: `uv run upstox_cli generate-token`
upx: UpstoxTOTP = UpstoxTOTP()

print("Getting Access Token...")

try:
    access_token: AccessTokenResponse = upx.app_token.get_access_token()

    print(access_token.model_dump_json(indent=2))
except Exception as e:
    print(f"Error: {e}")


print("\n✨ Done! Check out the examples folder for more advanced usage.")
