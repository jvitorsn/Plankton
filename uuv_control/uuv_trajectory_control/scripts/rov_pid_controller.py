#!/usr/bin/env python3
# Copyright (c) 2016-2019 The UUV Simulator Authors.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import rclpy
import numpy as np
from uuv_control_interfaces import DPPIDControllerBase


class ROV_PIDController(DPPIDControllerBase):
    """PID controller for the dynamic positioning of ROVs."""

    _LABEL = 'PID'
    def __init__(self, node_name):
        self._tau = np.zeros(6)
        DPPIDControllerBase.__init__(self, node_name, False)
        self._is_init = True

    # =========================================================================
    def update_controller(self):
        if not self._is_init:
            return False
        # Update PID control action
        self._tau = self.update_pid()
        self.publish_control_wrench(self._tau)
        return True


# =============================================================================
def main():
    print('Starting PID')
    rclpy.init()

    try:
        node = ROV_PIDController('rov_pid_controller')
        rclpy.spin(node)
    except Exception as e:
        print('Caught exception: ' + str(e))
    finally:
        if rclpy.ok():
            rclpy.shutdown()
    print('Exiting')


# =============================================================================
if __name__ == '__main__':
    main()
