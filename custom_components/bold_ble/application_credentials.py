"""Application credentials platform for Bold BLE."""
import logging
from typing import Any

from aiohttp import ClientSession

from homeassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    BOLD_AUTHORIZE_URL,
    BOLD_REDIRECT_URI,
    BOLD_TOKEN_URL,
    CLIENT_ID,
    CLIENT_SECRET,
)

_LOGGER = logging.getLogger(__name__)


class OAuth2Impl(AuthImplementation):
    """Custom OAuth2 implementation for Bold."""

    def __init__(
        self,
        hass: HomeAssistant,
        auth_domain: str,
        credential: ClientCredential,
        authorization_server: AuthorizationServer,
    ) -> None:
        """Initialize Bold OAuth2 implementation."""
        super().__init__(hass, auth_domain, credential, authorization_server)
        self.session = async_get_clientsession(hass)

    @property
    def redirect_uri(self) -> str:
        """Return the redirect URI."""
        return BOLD_REDIRECT_URI

async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return OAuth2Impl(
        hass,
        auth_domain,
        credential,
        AuthorizationServer(
            authorize_url=BOLD_AUTHORIZE_URL,
            token_url=BOLD_TOKEN_URL,
        ),
    )
