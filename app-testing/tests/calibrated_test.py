"""Test the initial state the application with various setups."""
import logging
import os
from pathlib import Path
import time
from pytest import FixtureRequest
from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.menus.left_menu import LeftMenu
from src.menus.robots_list import RobotsList
from src.pages.robot_page import RobotPage
from src.menus.protocol_file import ProtocolFile
from src.pages.deck_calibrate import DeckCalibration
from src.resources.ot_robot import OtRobot
from src.resources.ot_application import OtApplication
from src.pages.overview import Overview
from src.driver.drag_drop import drag_and_drop_file

logger = logging.getLogger(__name__)


def test_calibrate(
    chrome_options: Options, test_protocols: Dict[str, Path], request: FixtureRequest
) -> None:
    """Upload a protocol."""
    robot = OtRobot()
    # expecting docker emulated robot
    assert robot.is_alive(), "is a robot available?"
    # use variable to prevent the popup
    os.environ["OT_APP_ANALYTICS__SEEN_OPT_IN"] = "true"
    # app can see docker robot
    os.environ["OT_APP_DISCOVERY__CANDIDATES"] = "localhost"
    with webdriver.Chrome(options=chrome_options) as driver:
        logger.debug(f"driver capabilities {driver.capabilities}")
        ot_application = OtApplication(
            Path(f"{driver.capabilities['chrome']['userDataDir']}/config.json")
        )
        logger.info(ot_application.config)
        # ignore updates
        ot_application.config["alerts"]["ignored"] = ["appUpdateAvailable"]
        ot_application.write_config()
        robots_list = RobotsList(driver)
        if not robots_list.is_robot_toggle_active(RobotsList.DEV):
            robots_list.get_robot_toggle(RobotsList.DEV).click()
        # calibrate
        robot_page = RobotPage(driver)
        # Check if calibration state. If calibration is started
        # but not finished, exit and start over
        calibrate = DeckCalibration(driver)
        exit_button = calibrate.exit_button()
        if exit_button:
            exit_button.click()
            calibrate.exit_confirm_button().click()
        driver.save_screenshot(
            f"results/{request.node.originalname}.before_start_calibration.png"
        )
        robot_page.start_calibration()
        calibrate.calibrate_deck()
        assert robot_page.wait_for_deck_to_show_calibrated()
        left_menu = LeftMenu(driver)
        left_menu.click_protocol_upload_button()
        protocol_file = ProtocolFile(driver)
        logger.info(f"uploading protocol: {test_protocols['python1'].resolve()}")
        input = protocol_file.get_drag_and_drop()
        drag_and_drop_file(input, test_protocols["python1"])
        time.sleep(2)
        overview = Overview(driver)
        overview.click_continue_if_present()
        # This element location will fail if the file is not loaded.
        overview.get_filename_header(test_protocols["python1"].name)
        driver.save_screenshot(
            f"results/{request.node.originalname}.after_file_upload.png"
        )
