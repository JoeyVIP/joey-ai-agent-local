from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # LINE Bot
    line_channel_secret: str = Field(..., description="LINE Channel Secret")
    line_channel_access_token: str = Field(..., description="LINE Channel Access Token")
    joey_line_user_id: str = Field(..., description="Joey's LINE User ID for push notifications")

    # Notion
    notion_api_key: str = Field(..., description="Notion Integration Token")
    notion_inbox_db_id: str = Field(..., description="Notion Inbox Database ID")
    notion_review_db_id: str = Field(..., description="Notion Review Database ID")
    notion_memory_db_id: str = Field(..., description="Notion Memory Database ID")

    # Anthropic
    anthropic_api_key: str = Field(..., description="Anthropic API Key")
    anthropic_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Claude model to use"
    )

    # Claude Code
    claude_code_oauth_token: str = Field(
        default="",
        description="Claude Code OAuth Token for headless/SSH execution"
    )

    # External Service Tokens (used by MCP servers)
    github_token: str = Field(
        default="",
        description="GitHub Personal Access Token"
    )
    railway_token: str = Field(
        default="",
        description="Railway API Token (deprecated, use Render)"
    )
    render_api_key: str = Field(
        default="",
        description="Render API Key for deployment"
    )

    # App
    app_env: str = Field(default="development", description="Application environment")
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore any extra env vars not defined here


settings = Settings()
