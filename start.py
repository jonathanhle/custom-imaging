# Copyright 2019 Palo Alto Networks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from lib.script_logger import Logger
from lib.utils import CustomAmi


CONFIG_FILE = "config.yaml"


def main():

    # Custom AMI library Initialization
    lib = CustomAmi(logger, 'aws', CONFIG_FILE)

    # Create a base Instance(EC2)
    lib.cloud_client.create_instance()

    try:
        # Connect to FW Instance
        lib.connect_to_vmseries()

        # License the FW
        lib.license_firewall()

        # Verify System
        lib.verify_system()

        # Upgrade Content
        lib.upgrade_content()

        # Upgrade Anti-virus
        lib.upgrade_antivirus()

        # Upgrade Global-Protect Clientless VPN
        lib.upgrade_gp_cvpn()

        # Upgrade Wildfire
        lib.upgrade_wildfire()

        # Upgrade VM Series Plugin
        lib.upgrade_plugin()

        # Upgrade PanOS
        lib.upgrade_panos()

        # Verify Upgrades
        lib.verify_upgrades()

        # Perform Private Data Reset
        lib.private_data_reset()

        # Verify Upgrades after Private Data Reset
        lib.verify_upgrades()

        # Close connection to the Firewall
        lib.handler.close()

        # Create Custom AMI
        lib.create_custom_ami()

        # Cleanup
        logger.info('*** Terminating Base Instance ***')
        lib.cloud_client.terminate_instance()
        logger.info('*** Termination Complete ***')

    except Exception as e:
        # Failed
        logger.error(f'*** Failed to Create Custom AMI ***')
        logger.error(f'TRACEBACK: {str(e)}')
        # Terminating created Instance(EC2)
        logger.info('*** Terminating Base Instance ***')
        lib.cloud_client.terminate_instance()
        logger.info('*** Termination Complete ***')


if __name__ == '__main__':
    # Setup Logger
    logger = Logger(console=True)
    # Create Custom AMI
    main()
