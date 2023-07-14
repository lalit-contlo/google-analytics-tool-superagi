import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from datetime import date
from getMetricDimensions import getMetric, getDim
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

class UserReportInput(BaseModel):
    day = date.today()
    met: str = Field(..., description="The metric the user wants to know, for example number of active users")
    dim: str = Field(..., description="The context or dimension for which the user wants to know, for example, a city")
    start: str = Field(..., description="The starting date of the query, in YYYY-MM-DD format")
    end: str = Field(..., description=f"The last date of the query, in YYYY-MM-DD format, if today, return {day}")


class reportTool(BaseTool):
    """
    Analytics Report Tool
    """
    name: str = "Analytics Report Tool"
    args_schema: Type[BaseModel] = UserReportInput
    description: str = "Return a google analytics report for the information the user requires"

    def _execute(self, met, dim, start, end):
        from_name = self.get_tool_config('GOOGLE_APPLICATION_CREDS')
        pid=os.environ('property_id')
        client = BetaAnalyticsDataClient()

        m = getMetric(met)
        d = getDim(dim)
        mi=[]
        for x in m:
            mi.append(Metric(name=x))
        di = []
        for x in d:
            di.append(Dimension(name=x))
        request = RunReportRequest(
            property=f"properties/{pid}",
            dimensions=[Dimension(name=d[0])],
            metrics=[Metric(name=m[0])],
            date_ranges=[DateRange(start_date=start, end_date=end)],
        )
        response = client.run_report(request)

        str = ""
        for row in response.rows:
            str = str + "\n" + row.dimension_values[0].value + " " + row.metric_values[0].value

        return str