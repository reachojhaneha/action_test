"""Model for the screen of Multiples of a Module."""
import logging
from typing import Tuple
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.driver.highlight import highlight

logger = logging.getLogger(__name__)


class MoamPur:
    """Class for Moam Setup flow."""

    def __init__(self, driver: WebDriver) -> None:
        """Initialize with driver."""
        self.driver: WebDriver = driver

    organization_author_text_locator: Tuple[str, str] = (
        By.ID,
        "MetadataCard_protocolOrganizationAuthor",
    )
    description_text_locator: Tuple[str, str] = (
        By.ID,
        "MetadataCard_protocolDescription",
    )
    attach_pipette_button: Tuple[str, str] = (
        By.ID,
        "PipetteCalibration_attachPipetteButton",
    )
    moam_link: Tuple[str, str] = (
        By.XPATH,
        "//a[text()='See How To Set Up Modules of the Same Type']",
    )
    moam_modal_text_locator: Tuple[str, str] = (
        By.XPATH,
        "//h3[text()='Setting Up Modules of the Same Type']",
    )
    close_protocol_text_locator: Tuple[str, str] = (
        By.XPATH,
        "//button[text()='close']",
    )
    yes_close_now_text_locator: Tuple[str, str] = (
        By.XPATH,
        "//button[text()='Yes, close now']",
    )

    @highlight
    def get_organization_author_text(self) -> WebElement:
        """Locator for organization author text."""
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(MoamPur.organization_author_text_locator)
        )

    @highlight
    def get_description_text(self) -> WebElement:
        """Locator for description text locator."""
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(MoamPur.description_text_locator)
        )

    @highlight
    def get_attach_pipette_button(self) -> WebElement:
        """Locator for magnetic module on deckmap."""
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(MoamPur.attach_pipette_button)
        )

    @highlight
    def get_moam_link(self) -> WebElement:
        """Locator for multiples of module link."""
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(MoamPur.moam_link)
        )

    @highlight
    def get_moam_modal_text(self) -> WebElement:
        """Locator for moam modal text."""
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(MoamPur.moam_modal_text_locator)
        )

    @highlight
    def get_protocol_close_button(self) -> WebElement:
        """Locator for close protocol button."""
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(MoamPur.close_protocol_text_locator)
        )

    @highlight
    def get_confirmation_close_button(self) -> WebElement:
        """Locator for yes close now button."""
        return WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(MoamPur.yes_close_now_text_locator)
        )

    def click_moam_link(self) -> None:
        self.get_moam_link().click()

    def click_protocol_close_button(self) -> None:
        self.get_protocol_close_button().click()

    def click_confirmation_close_button(self) -> None:
        self.get_confirmation_close_button().click()
