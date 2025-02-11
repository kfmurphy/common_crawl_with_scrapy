#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on JAN 05 18:36:08 2023

This can ge requested from common-crawl endpoint for the latest updates.

@author: KFM
"""

CDX = [
    {
      "id": "CC-MAIN-2022-49",
      "name": "November/December 2022 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2022-49/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2022-49-index"
    },
    {
      "id": "CC-MAIN-2022-40",
      "name": "September/October 2022 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2022-40/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2022-40-index"
    },
    {
      "id": "CC-MAIN-2022-33",
      "name": "August 2022 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2022-33/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2022-33-index"
    },
    {
      "id": "CC-MAIN-2022-27",
      "name": "June/July 2022 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2022-27/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2022-27-index"
    },
    {
      "id": "CC-MAIN-2022-21",
      "name": "May 2022 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2022-21/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2022-21-index"
    },
    {
      "id": "CC-MAIN-2022-05",
      "name": "January 2022 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2022-05/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2022-05-index"
    },
    {
      "id": "CC-MAIN-2021-49",
      "name": "November/December 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-49/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-49-index"
    },
    {
      "id": "CC-MAIN-2021-43",
      "name": "October 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-43/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-43-index"
    },
    {
      "id": "CC-MAIN-2021-39",
      "name": "September 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-39/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-39-index"
    },
    {
      "id": "CC-MAIN-2021-31",
      "name": "July/August 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-31/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-31-index"
    },
    {
      "id": "CC-MAIN-2021-25",
      "name": "June 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-25/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-25-index"
    },
    {
      "id": "CC-MAIN-2021-21",
      "name": "May 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-21/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-21-index"
    },
    {
      "id": "CC-MAIN-2021-17",
      "name": "April 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-17/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-17-index"
    },
    {
      "id": "CC-MAIN-2021-10",
      "name": "February/March 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-10/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-10-index"
    },
    {
      "id": "CC-MAIN-2021-04",
      "name": "January 2021 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2021-04/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2021-04-index"
    },
    {
      "id": "CC-MAIN-2020-50",
      "name": "November/December 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-50/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-50-index"
    },
    {
      "id": "CC-MAIN-2020-45",
      "name": "October 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-45/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-45-index"
    },
    {
      "id": "CC-MAIN-2020-40",
      "name": "September 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-40/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-40-index"
    },
    {
      "id": "CC-MAIN-2020-34",
      "name": "August 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-34/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-34-index"
    },
    {
      "id": "CC-MAIN-2020-29",
      "name": "July 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-29/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-29-index"
    },
    {
      "id": "CC-MAIN-2020-24",
      "name": "May/June 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-24/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-24-index"
    },
    {
      "id": "CC-MAIN-2020-16",
      "name": "March/April 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-16/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-16-index"
    },
    {
      "id": "CC-MAIN-2020-10",
      "name": "February 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-10/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-10-index"
    },
    {
      "id": "CC-MAIN-2020-05",
      "name": "January 2020 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2020-05/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2020-05-index"
    },
    {
      "id": "CC-MAIN-2019-51",
      "name": "December 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-51/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-51-index"
    },
    {
      "id": "CC-MAIN-2019-47",
      "name": "November 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-47/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-47-index"
    },
    {
      "id": "CC-MAIN-2019-43",
      "name": "October 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-43/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-43-index"
    },
    {
      "id": "CC-MAIN-2019-39",
      "name": "September 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-39/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-39-index"
    },
    {
      "id": "CC-MAIN-2019-35",
      "name": "August 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-35/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-35-index"
    },
    {
      "id": "CC-MAIN-2019-30",
      "name": "July 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-30/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-30-index"
    },
    {
      "id": "CC-MAIN-2019-26",
      "name": "June 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-26/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-26-index"
    },
    {
      "id": "CC-MAIN-2019-22",
      "name": "May 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-22/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-22-index"
    },
    {
      "id": "CC-MAIN-2019-18",
      "name": "April 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-18/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-18-index"
    },
    {
      "id": "CC-MAIN-2019-13",
      "name": "March 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-13/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-13-index"
    },
    {
      "id": "CC-MAIN-2019-09",
      "name": "February 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-09/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-09-index"
    },
    {
      "id": "CC-MAIN-2019-04",
      "name": "January 2019 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2019-04/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2019-04-index"
    },
    {
      "id": "CC-MAIN-2018-51",
      "name": "December 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-51/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-51-index"
    },
    {
      "id": "CC-MAIN-2018-47",
      "name": "November 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-47/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-47-index"
    },
    {
      "id": "CC-MAIN-2018-43",
      "name": "October 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-43/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-43-index"
    },
    {
      "id": "CC-MAIN-2018-39",
      "name": "September 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-39/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-39-index"
    },
    {
      "id": "CC-MAIN-2018-34",
      "name": "August 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-34/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-34-index"
    },
    {
      "id": "CC-MAIN-2018-30",
      "name": "July 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-30/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-30-index"
    },
    {
      "id": "CC-MAIN-2018-26",
      "name": "June 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-26/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-26-index"
    },
    {
      "id": "CC-MAIN-2018-22",
      "name": "May 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-22/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-22-index"
    },
    {
      "id": "CC-MAIN-2018-17",
      "name": "April 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-17/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-17-index"
    },
    {
      "id": "CC-MAIN-2018-13",
      "name": "March 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-13/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-13-index"
    },
    {
      "id": "CC-MAIN-2018-09",
      "name": "February 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-09/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-09-index"
    },
    {
      "id": "CC-MAIN-2018-05",
      "name": "January 2018 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2018-05/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2018-05-index"
    },
    {
      "id": "CC-MAIN-2017-51",
      "name": "December 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-51/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-51-index"
    },
    {
      "id": "CC-MAIN-2017-47",
      "name": "November 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-47/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-47-index"
    },
    {
      "id": "CC-MAIN-2017-43",
      "name": "October 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-43/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-43-index"
    },
    {
      "id": "CC-MAIN-2017-39",
      "name": "September 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-39/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-39-index"
    },
    {
      "id": "CC-MAIN-2017-34",
      "name": "August 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-34/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-34-index"
    },
    {
      "id": "CC-MAIN-2017-30",
      "name": "July 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-30/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-30-index"
    },
    {
      "id": "CC-MAIN-2017-26",
      "name": "June 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-26/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-26-index"
    },
    {
      "id": "CC-MAIN-2017-22",
      "name": "May 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-22/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-22-index"
    },
    {
      "id": "CC-MAIN-2017-17",
      "name": "April 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-17/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-17-index"
    },
    {
      "id": "CC-MAIN-2017-13",
      "name": "March 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-13/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-13-index"
    },
    {
      "id": "CC-MAIN-2017-09",
      "name": "February 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-09/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-09-index"
    },
    {
      "id": "CC-MAIN-2017-04",
      "name": "January 2017 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2017-04/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2017-04-index"
    },
    {
      "id": "CC-MAIN-2016-50",
      "name": "December 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-50/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-50-index"
    },
    {
      "id": "CC-MAIN-2016-44",
      "name": "October 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-44/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-44-index"
    },
    {
      "id": "CC-MAIN-2016-40",
      "name": "September 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-40/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-40-index"
    },
    {
      "id": "CC-MAIN-2016-36",
      "name": "August 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-36/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-36-index"
    },
    {
      "id": "CC-MAIN-2016-30",
      "name": "July 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-30/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-30-index"
    },
    {
      "id": "CC-MAIN-2016-26",
      "name": "June 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-26/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-26-index"
    },
    {
      "id": "CC-MAIN-2016-22",
      "name": "May 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-22/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-22-index"
    },
    {
      "id": "CC-MAIN-2016-18",
      "name": "April 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-18/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-18-index"
    },
    {
      "id": "CC-MAIN-2016-07",
      "name": "February 2016 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2016-07/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2016-07-index"
    },
    {
      "id": "CC-MAIN-2015-48",
      "name": "November 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-48/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-48-index"
    },
    {
      "id": "CC-MAIN-2015-40",
      "name": "September 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-40/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-40-index"
    },
    {
      "id": "CC-MAIN-2015-35",
      "name": "August 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-35/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-35-index"
    },
    {
      "id": "CC-MAIN-2015-32",
      "name": "July 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-32/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-32-index"
    },
    {
      "id": "CC-MAIN-2015-27",
      "name": "June 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-27/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-27-index"
    },
    {
      "id": "CC-MAIN-2015-22",
      "name": "May 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-22/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-22-index"
    },
    {
      "id": "CC-MAIN-2015-18",
      "name": "April 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-18/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-18-index"
    },
    {
      "id": "CC-MAIN-2015-14",
      "name": "March 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-14/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-14-index"
    },
    {
      "id": "CC-MAIN-2015-11",
      "name": "February 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-11/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-11-index"
    },
    {
      "id": "CC-MAIN-2015-06",
      "name": "January 2015 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2015-06/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2015-06-index"
    },
    {
      "id": "CC-MAIN-2014-52",
      "name": "December 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-52/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-52-index"
    },
    {
      "id": "CC-MAIN-2014-49",
      "name": "November 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-49/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-49-index"
    },
    {
      "id": "CC-MAIN-2014-42",
      "name": "October 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-42/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-42-index"
    },
    {
      "id": "CC-MAIN-2014-41",
      "name": "September 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-41/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-41-index"
    },
    {
      "id": "CC-MAIN-2014-35",
      "name": "August 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-35/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-35-index"
    },
    {
      "id": "CC-MAIN-2014-23",
      "name": "July 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-23/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-23-index"
    },
    {
      "id": "CC-MAIN-2014-15",
      "name": "April 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-15/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-15-index"
    },
    {
      "id": "CC-MAIN-2014-10",
      "name": "March 2014 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2014-10/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2014-10-index"
    },
    {
      "id": "CC-MAIN-2013-48",
      "name": "Winter 2013 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2013-48/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2013-48-index"
    },
    {
      "id": "CC-MAIN-2013-20",
      "name": "Summer 2013 Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2013-20/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2013-20-index"
    },
    {
      "id": "CC-MAIN-2012",
      "name": "2012 ARC Files Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2012/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2012-index"
    },
    {
      "id": "CC-MAIN-2009-2010",
      "name": "2009 - 2010 ARC Files Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2009-2010/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2009-2010-index"
    },
    {
      "id": "CC-MAIN-2008-2009",
      "name": "2008 - 2009 ARC Files Index",
      "timegate": "https://index.commoncrawl.org/CC-MAIN-2008-2009/",
      "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2008-2009-index"
    }
  ]