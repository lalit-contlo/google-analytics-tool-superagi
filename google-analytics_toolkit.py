from abc import ABC
import os
from superagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from typing import List
from userReport import reportTool
from superagi.types.key_type import ToolConfigKeyType

class AnalyticsToolkit(BaseToolkit, ABC):
    name: str = "Google Analytics Toolkit"
    description: str = "Google Analytics Toolkit returns google analytics reports requested by the user"

    def get_tools(self) -> List[BaseTool]:
        return [reportTool()]

    def get_env_keys(self) -> List[str]:
        return [
            ToolConfiguration(key="PROPERTY_ID", key_type=ToolConfigKeyType.STRING, is_required=True,
                              is_secret=True),
            ToolConfiguration(key="GOOGLE_APPLICATION_CREDENTIALS", key_type=ToolConfigKeyType.FILE, is_required=True,
                              is_secret=False)
        ]